---
name: component-reuse-first
description: Search existing components before creating new ones. When a new component is unavoidable, design it for future reuse with proper props, composition, and placement in shared directories. Use when building UI, creating React/Vue/Svelte/Angular/SwiftUI components, adding buttons/forms/cards/modals/tables, scaffolding pages, or any time the user says "create a component", "add a component", "build a UI", or mentions component-like work.
---

# Component Reuse First

Before creating any UI component, exhaustively check whether an existing component (or close variant) already covers the need. Only create a new component when reuse is genuinely impossible — and when you do, design it to be reused next time.

## Core Workflow

### 1. Search Before Create (mandatory)

Run all of these in parallel before writing any new component:

- **Glob** common component directories:
  - `**/components/**/*.{tsx,jsx,ts,js,vue,svelte}`
  - `**/ui/**/*.{tsx,jsx,vue,svelte}`
  - `**/shared/**/*.{tsx,jsx,vue,svelte}`
  - `**/design-system/**/*`, `**/lib/components/**/*`
- **Grep** for the conceptual name and synonyms:
  - User asks for "Modal" → grep `Modal|Dialog|Popup|Overlay|Sheet|Drawer`
  - User asks for "Button" → grep `Button|Btn|IconButton|CTA`
  - User asks for "Card" → grep `Card|Panel|Tile|Box`
  - User asks for "Input" → grep `Input|TextField|TextInput|FormField`
  - User asks for "List" → grep `List|Table|DataGrid|Items`
- **Check imports** in similar pages/features for what they already use
- **Check the package.json** for design system libraries (shadcn/ui, MUI, Chakra, Mantine, Ant, Radix, HeroUI, NextUI, Tamagui, native-base, etc.) — prefer those over hand-rolling

### 2. Decision Tree

After search:

- **Exact match exists** → Reuse as-is. Do not duplicate.
- **Close match exists (90%+)** → Extend the existing component via props/variants. Do not fork.
- **Partial match exists** → Refactor existing into base + variant, or compose. Avoid copy-paste.
- **Nothing matches** → Create new, following the Reusable-by-Default rules below.

State the decision explicitly to the user before coding: e.g. "Found `Button` at `src/ui/Button.tsx` with `variant` prop — adding `ghost` variant" or "No matching modal — creating new `Modal` at `src/ui/Modal.tsx`."

### 3. Reusable-by-Default Rules (when creating new)

When a new component is necessary, build it for the next caller, not just this one:

**Placement**
- Shared/generic → `components/ui/`, `src/ui/`, or the project's design-system path
- Feature-scoped (only meaningful inside one feature) → `features/<feature>/components/`
- Never put a reusable primitive inside a route/page file

**API design**
- Accept `className` and forward refs (React: `forwardRef` + `cn(className)` pattern)
- Spread rest props to the underlying element (`...props` / `v-bind="$attrs"`)
- Use **variants** (e.g. `cva`, `tv`, prop unions) instead of duplicating components
- Children/slots over hardcoded content
- Use semantic prop names (`variant`, `size`, `tone`, `intent`) — not visual ones (`bigBlueButton`)
- Required vs optional props: keep required surface minimal; sensible defaults for the rest

**Composition over configuration**
- Prefer compound components (`Card.Header`, `Card.Body`) over giant prop bags
- Slot/children patterns beat dozens of `*Content` props

**Styling**
- Match the project's existing approach (Tailwind, CSS modules, styled-components, vanilla-extract). Do not introduce a new styling system.
- Use design tokens / theme values, not hard-coded colors or spacings

**Type safety (TS projects)**
- Extend native element props: `ButtonHTMLAttributes<HTMLButtonElement>`
- Discriminated unions for variants when behavior differs (e.g. `as="link" | "button"`)

**Accessibility**
- Correct semantic element by default (button vs div)
- ARIA attributes wired through props
- Keyboard interaction handled at the primitive level

### 4. After Creating

- Export from the directory's `index.ts` barrel (if the project uses one)
- Add to Storybook / docs if the project has them
- If you noticed during search that *several* existing components could now be replaced by the new one, mention it to the user (don't refactor unprompted)

## Anti-patterns to Refuse

- ❌ Creating `Button2`, `NewButton`, `CustomButton` next to existing `Button`
- ❌ Inline-defining a component inside a page when it's clearly reusable
- ❌ Copy-pasting a component to tweak two lines instead of adding a prop
- ❌ Hardcoded copy/colors/sizes that prevent reuse
- ❌ Introducing a second design system / UI lib when one is already in use
- ❌ Skipping the search step "because the component is simple"

## Quick Heuristics

- If you typed `function Button(` and a `Button` already exists in the repo → stop, reuse.
- If your new component has zero props → it's probably not reusable; ask if it should accept content/variants.
- If you're about to write the same JSX you saw 20 minutes ago in another file → extract it.

## Example Interactions

**User:** "Add a confirmation modal for the delete action."
**You:** Grep for `Modal|Dialog|Confirm`. Found `ConfirmDialog` at `src/ui/ConfirmDialog.tsx`. → Reuse it; pass `title`, `onConfirm`, `destructive` props.

**User:** "Create a pricing card component."
**You:** Grep for `Card`. Found `Card` primitive in `src/ui/Card.tsx`. → Compose `PricingCard` from `Card` + `Card.Header` + `Card.Body`; place in `features/pricing/components/`. Don't reinvent the card frame.

**User:** "I need a button with a loading spinner."
**You:** Grep for `Button`. Found one without `loading` prop. → Add `loading?: boolean` prop to existing `Button`; do not create `LoadingButton`.

## Activation Triggers

This skill should activate whenever the conversation involves:
- Creating, building, scaffolding, or adding a UI component
- Words: component, button, modal, dialog, card, form, input, table, list, dropdown, menu, sidebar, header, footer, layout, page, view, screen, widget
- Frameworks: React, Vue, Svelte, Angular, Solid, SwiftUI, Jetpack Compose, Flutter
- Phrases: "make a", "build a", "I need a", "create a", "add a" + UI noun
