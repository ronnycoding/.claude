# Claude Commands Reference

## Available Commands

### `/nlm-research` - NotebookLM Research Generator

Generate comprehensive research reports, analysis, and documentation using Google NotebookLM with support for multiple sources and output formats.

**Usage:**
```bash
claude nlm-research --project="Acme SaaS" --type=mvp-design \
  --urls="https://competitor1.com" \
  --files="./requirements.pdf" \
  --outputs="guide,audio" \
  --save-to="./research/acme-mvp"
```

**Research Types:**
- `mvp-design` - MVP product design with features, tech stack, timeline
- `market-analysis` - Market research, competitors, trends, opportunities
- `technical-doc` - Technical documentation and architecture guides
- `business-plan` - Business strategy, financials, go-to-market
- `competitive-intel` - Deep competitor analysis with SWOT
- `custom` - Flexible research with custom instructions

**Input Sources:**
- `--urls` - Web pages and articles (comma-separated)
- `--files` - Local PDFs, docs, markdown files
- `--docs` - Google Docs share links
- `--text` - Direct text content

**Output Options:**
- `guide` - Comprehensive structured summary
- `outline` - Hierarchical topic structure
- `section` - Focused content sections
- `audio` - AI-generated audio overview with transcript
- `all` - Generate everything

**Features:**
- Multi-source aggregation with rate limiting
- Automated workflow from setup to export
- Customizable audio tone and audience
- Organized directory structure with timestamps
- Quality assurance and error handling

See `nlm-research.md` for complete documentation and examples.

---

### `/tiktok-tech` - TikTok Tech News Digest Generator

Generate comprehensive, news-style TikTok scripts covering multiple tech stories in one unified video.

**Usage:**
```bash
/tiktok-tech [Paste your weekly tech digest or multiple tech stories here]
```

**Format:** Single comprehensive news digest (90-120 seconds)

**Features:**
- **News Anchor Style**: Professional presenter format with personality
- **Comprehensive Coverage**: 3-5 interconnected stories in one video
- **Unified Narrative**: Connects the dots between developments
- **Analysis Section**: Industry implications and bigger picture
- **BILINGUAL**: Complete scripts in English AND Spanish
- **Professional Production**: B-roll, graphics, lower thirds suggestions
- **Actionable Takeaways**: What developers should do with this info

**Output includes:**
- Complete dialogue with precise timing marks (00:00 format)
- Visual cues and B-roll library suggestions
- Story transition cues
- Lower thirds and text overlay recommendations
- Analysis connecting all stories
- Production notes (music, background, hashtags)
- Full Spanish version with cultural adaptations
- Professional enough to share with your team
- **Auto-saved markdown file** in `docs/tiktok-scripts/` directory

---

### `/issue` - GitHub Issue Creation

Creates comprehensive GitHub issues with sub-issue decomposition.

---

### `/pr` - GitHub Pull Request Creation

Generates well-structured pull requests following repo conventions.

---

### `/todos` - Todo Management

Advanced todo tracking with agent orchestration support.

---

### `/task` - Task Management

General task tracking and management.

---

## Examples

### TikTok Tech News Digest Example

```bash
/tiktok-tech Vercel launched AI agents marketplace. LangChain clarified Framework vs Runtime vs Harness. Python 3.14 removed GIL for true async parallelism. Microsoft Edge released agentic browsing. Cloudflare partnered with Visa/Mastercard for AI agent transactions.
```

**This generates ONE comprehensive 90-120s script covering:**
- Opening hook tying all stories together
- Each story with proper context and explanation
- Smooth transitions between topics
- Analysis of how these stories interconnect
- What it means for the AI agent ecosystem
- Developer action items
- Full English script with timing
- Complete Spanish translation
- Production guide for filming

**Perfect for:**
- Weekly tech roundups
- Industry trend analysis
- Multi-story deep dives
- Educational tech content
- Professional developer updates

---

## Tips

- **Paste multiple stories**: The more context, the better the connections
- **Include dates**: Helps establish timeline and urgency
- **Add source links**: Improves accuracy and attribution
- **Provide full context**: Better analysis comes from comprehensive input
- **Weekly digests work best**: 3-5 related stories create compelling narrative

