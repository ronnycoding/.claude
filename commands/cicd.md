---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: [target-dir | notes about the stack/deploy target]
description: Scaffold GitHub Actions + Terraform IaC for a chosen cloud provider, with keyless OIDC auth, remote state, and plan-on-PR / apply-on-main pipelines.
---

# CI/CD Bootstrap — GitHub Actions + Terraform

You are an AI assistant that sets up production-grade CI/CD for the current repository: **GitHub Actions** workflows driving **Terraform** infrastructure-as-code against a user-selected cloud provider. Use the **AskUserQuestion** tool to resolve every decision that can't be confidently inferred from the repo.

The canonical reference pattern is a GCP stack (Cloud Run + Cloud SQL + Firebase) using keyless Workload Identity Federation, GCS remote state, and a `terraform.yml` that plans on PR and applies on main. Mirror these patterns and adapt them to the chosen provider.

## Input

<notes>
$ARGUMENTS
</notes>

`$ARGUMENTS` is optional free-text (a target subdirectory, the app type, or deploy-target hints). Treat it as context, not a strict spec.

---

## Non-negotiable principles

- **Keyless auth by default.** Use GitHub OIDC → cloud federation (GCP Workload Identity Federation, AWS IAM OIDC role, Azure federated credentials). Never write long-lived cloud keys into the repo. Only fall back to a stored credential secret if the user explicitly opts in.
- **Remote, locked state.** Provision/declare a remote backend (GCS / S3+DynamoDB / azurerm) — never local state in CI.
- **Plan on PR, apply on main.** PRs run `terraform plan` and post the result as a PR comment; pushes to the default branch run `terraform apply -auto-approve`. Never run `terraform destroy` in a workflow.
- **One run at a time.** Use a `concurrency` group so state-mutating jobs can't race (`cancel-in-progress: false`).
- **Least privilege.** Set explicit `permissions:` per workflow (`id-token: write`, `contents: read`, `pull-requests: write` only where needed).
- **Pin versions.** Pin `TF_VERSION` and action versions (`@v4`, etc.).
- **Real tooling only.** `gh`, `git`, `terraform`/`tofu`, cloud CLIs. Don't invent commands.

---

## Phase 1 — Discover the repository

Before asking anything, inspect what already exists so questions are informed and you don't duplicate config:

```bash
gh repo view --json nameWithOwner,defaultBranchRef -q '{repo: .nameWithOwner, branch: .defaultBranchRef.name}'
ls -la .github/workflows/ 2>/dev/null
find . -maxdepth 2 -name '*.tf' -o -name 'main.tf' 2>/dev/null
```

Detect: language/runtime & build tooling (package.json, pyproject/requirements, go.mod, Dockerfile, etc.), existing workflows, any existing `terraform/` dir and backend, and probable deploy artifacts (container image vs. static site vs. serverless function). Summarize findings to the user in 3-5 lines before the questions.

## Phase 2 — Clarify with AskUserQuestion

Ask only what you can't infer. Batch related questions in a single `AskUserQuestion` call (it supports up to 4). Recommended questions:

1. **Cloud provider** — header `Provider`. Options: **GCP (Recommended — matches reference)**, **AWS**, **Azure**, (Other). This drives the provider block, backend, and auth method.
2. **Auth method** — header `Auth`. Options: **Keyless OIDC (Recommended)** (WIF / IAM OIDC role / federated cred), **Stored credentials secret** (only if OIDC isn't feasible).
3. **State backend** — header `State`. Options: **Managed remote (Recommended)** (create/declare GCS / S3+DynamoDB / azurerm), **Existing backend** (ask for bucket/prefix), **Local** (discouraged — dev only).
4. **What to deploy** — header `Deploy target`. multiSelect. Options derived from Phase 1: e.g. **Container service** (Cloud Run / ECS / Container Apps), **Static site/CDN**, **Serverless function**, **Database/managed services only (Terraform-only)**.

If the provider is GCP, also confirm **project id**, **region** (default `us-central1`), and **environments** (e.g. `prod` only, or `staging`+`prod`). For AWS confirm **account id** + **region**; for Azure **subscription id** + **resource group** + **location**. Use AskUserQuestion or, for free-form ids, ask inline.

## Phase 3 — Scaffold Terraform

Create a `terraform/` directory (or the dir from `$ARGUMENTS`) with:

- `backend.tf` — remote backend for the chosen provider.
- `providers.tf` / `versions.tf` — `required_providers` + pinned versions, `required_version`.
- `variables.tf` — `project_id`/`account_id`/`subscription_id`, `region`, environment, and per-target inputs.
- `main.tf` — root config wiring **modules** (`./modules/<resource>`), mirroring the reference's module-per-resource layout with explicit `depends_on`.
- `modules/<name>/{main.tf,variables.tf,outputs.tf}` for each selected deploy target.
- `*.tfvars.example` — documented, no secrets committed; add `*.tfvars` and `.terraform/` to `.gitignore`.

**Backend examples by provider:**

```hcl
# GCP
terraform { backend "gcs" { bucket = "<project>-tf-state" prefix = "terraform/state" } }

# AWS (state lock via DynamoDB)
terraform { backend "s3" { bucket = "<project>-tf-state" key = "terraform/state.tfstate" region = "<region>" dynamodb_table = "<project>-tf-locks" encrypt = true } }

# Azure
terraform { backend "azurerm" { resource_group_name = "<rg>" storage_account_name = "<sa>" container_name = "tfstate" key = "terraform.tfstate" } }
```

## Phase 4 — Generate GitHub Actions workflows

Write to `.github/workflows/`. Always create **`terraform.yml`** modeled on the reference; add app build/deploy workflows for the selected targets.

`terraform.yml` must:
- Trigger on `pull_request` and `push` to the default branch filtered to `paths: ['terraform/**']`, plus `workflow_dispatch`.
- Set `permissions: { contents: read, id-token: write, pull-requests: write }`.
- Use a `concurrency` group keyed on ref with `cancel-in-progress: false`.
- Authenticate via OIDC (provider-specific action), then `setup-terraform` with pinned `TF_VERSION` and `terraform_wrapper: true`.
- Run `init` → `validate` → (PR) `plan` with `continue-on-error: true` → post/update a **single** PR comment via `actions/github-script@v7` with a results table + collapsible plan, truncating output > ~65k chars → fail the step if plan failed → (push/dispatch on default branch) `apply -auto-approve`.

**OIDC auth step by provider:**

```yaml
# GCP
- uses: google-github-actions/auth@v2
  with: { workload_identity_provider: ${{ secrets.WIF_PROVIDER }}, service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }} }

# AWS
- uses: aws-actions/configure-aws-credentials@v4
  with: { role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}, aws-region: <region> }

# Azure
- uses: azure/login@v2
  with: { client-id: ${{ secrets.AZURE_CLIENT_ID }}, tenant-id: ${{ secrets.AZURE_TENANT_ID }}, subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }} }
```

For container targets, add a build/deploy workflow: build & push the image to the provider registry (Artifact Registry / ECR / ACR) using the same OIDC auth, then deploy (Cloud Run / ECS service / Container App). For static sites, build and deploy to the chosen hosting/CDN.

## Phase 5 — Validate & hand off the setup checklist

- If `terraform` (or `tofu`) is installed, run `terraform -chdir=terraform fmt -recursive` and `terraform -chdir=terraform validate` (after a backend-less `init -backend=false`) to catch syntax errors. Report results honestly.
- Print a **bootstrap checklist** the user must do once (these can't live in the repo):
  - Create the OIDC federation: GCP WIF pool+provider & service account, or AWS IAM OIDC provider+role with a trust policy scoped to `repo:<owner>/<repo>:ref:refs/heads/<branch>`, or Azure app registration + federated credential.
  - Create the state backend resource (bucket/table/storage account) — or confirm it exists.
  - Set repo secrets via `gh secret set` (e.g. `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`, or `AWS_DEPLOY_ROLE_ARN`, or `AZURE_*`). List the exact names you referenced.
  - Required GCP/AWS/Azure APIs/services enabled.
- Offer to commit on a branch and open a PR via **`/pr`** (don't push to the default branch directly).

---

## Reference: the `terraform.yml` shape (GCP, ACME example)

The pattern to replicate (plan-on-PR with sticky comment, apply-on-main, state-lock concurrency):

```yaml
name: Terraform
on:
  push: { branches: [main], paths: ['terraform/**'] }
  pull_request: { branches: [main], paths: ['terraform/**'] }
  workflow_dispatch:
env: { TF_VERSION: "1.9.8", REGION: us-central1, WORKING_DIR: terraform }
concurrency: { group: terraform-${{ github.ref }}, cancel-in-progress: false }
jobs:
  terraform:
    runs-on: ubuntu-latest
    permissions: { contents: read, id-token: write, pull-requests: write }
    defaults: { run: { working-directory: terraform } }
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with: { workload_identity_provider: ${{ secrets.WIF_PROVIDER }}, service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }} }
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: ${{ env.TF_VERSION }}, terraform_wrapper: true }
      - run: terraform init -input=false
      - run: terraform validate -no-color
      - id: plan
        if: github.event_name == 'pull_request'
        run: terraform plan -input=false -no-color
        continue-on-error: true
      # ... actions/github-script@v7 posts/updates one PR comment with the plan ...
      - if: (github.event_name == 'push' || github.event_name == 'workflow_dispatch') && github.ref == 'refs/heads/main'
        run: terraform apply -input=false -auto-approve
```
