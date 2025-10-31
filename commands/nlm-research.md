---
description: Generate comprehensive research reports using NotebookLM with support for multiple sources and output formats
args:
  - name: project
    description: Project or topic name (e.g., "Acme SaaS Platform")
    required: true
  - name: type
    description: Research type (mvp-design, market-analysis, technical-doc, business-plan, competitive-intel, custom)
    required: true
    default: custom
  - name: urls
    description: Comma-separated list of URLs to add as sources
    required: false
  - name: files
    description: Comma-separated list of file paths to add as sources
    required: false
  - name: docs
    description: Comma-separated list of Google Docs share links
    required: false
  - name: text
    description: Direct text content to add as a source
    required: false
  - name: outputs
    description: Comma-separated output types (guide, outline, section, audio, all)
    required: false
    default: guide,audio
  - name: audio-tone
    description: Audio tone (conversational, formal)
    required: false
    default: conversational
  - name: audio-audience
    description: Target audience (technical, general, executive)
    required: false
    default: general
  - name: save-to
    description: Directory path to save exported content
    required: false
---

# NotebookLM Research Command

You are an AI assistant specialized in conducting comprehensive research using Google NotebookLM. You will create structured research outputs including guides, outlines, and audio overviews based on multiple sources.

## Input Parameters

<project_name>
$PROJECT
</project_name>

<research_type>
$TYPE
</research_type>

<source_urls>
$URLS
</source_urls>

<source_files>
$FILES
</source_files>

<source_docs>
$DOCS
</source_docs>

<source_text>
$TEXT
</source_text>

<output_types>
$OUTPUTS
</output_types>

<audio_configuration>
Tone: $AUDIO_TONE
Audience: $AUDIO_AUDIENCE
</audio_configuration>

<export_directory>
$SAVE_TO
</export_directory>

## Workflow Instructions

Follow these phases systematically to complete the research task:

### Phase 1: Setup & Authentication

1. **Invoke NotebookLM Skill**
   - Use the Skill tool to load the NotebookLM skill: `notebooklm`
   - Wait for the skill to load and provide its instructions

2. **Authenticate**
   - Run: `nlm auth` to ensure authentication is valid
   - If authentication fails, prompt user to complete OAuth flow

3. **Create Research Notebook**
   - Generate a descriptive title with date: `[YYYY-MM-DD] $PROJECT - $TYPE`
   - Run: `nlm create "notebook-title"`
   - Capture the notebook ID for subsequent operations

### Phase 2: Source Aggregation

1. **Parse & Validate Sources**
   - Parse comma-separated URLs, files, docs, and text
   - Validate that at least one source type is provided
   - Check file paths exist before adding
   - Validate URL formats

2. **Add Sources with Rate Limiting**
   - For each source:
     - Add to notebook: `nlm add <notebook-id> <source>`
     - Wait 2-3 seconds between additions to respect rate limits
     - Log each successful addition
     - Handle errors gracefully (skip failed sources, continue)

3. **Rename Sources**
   - After all sources are added, list sources: `nlm sources <notebook-id>`
   - Rename each source with descriptive titles
   - Use prefixes: [URL], [PDF], [DOC], [TEXT]

### Phase 3: Research Type Configuration

Based on the `research_type`, configure the research focus and output instructions:

#### MVP Design (`mvp-design`)
**Focus Areas:**
- Core features and functionality
- Technical architecture and stack recommendations
- User experience and interface design
- Development phases and timeline
- Resource requirements and team structure
- Success metrics and KPIs

**Audio Instructions:**
> "Create an engaging overview of this MVP product design. Focus on the core value proposition, key features, technical approach, and go-to-market strategy. Discuss the development roadmap and critical success factors. Audience: $AUDIO_AUDIENCE, Tone: $AUDIO_TONE"

#### Market Analysis (`market-analysis`)
**Focus Areas:**
- Market size, growth trends, and forecasts
- Target audience segments and personas
- Competitive landscape and positioning
- Industry trends and disruptions
- Opportunities and threats
- Market entry strategy

**Audio Instructions:**
> "Provide a comprehensive market analysis discussion. Cover market size and trends, competitive dynamics, target customer segments, and strategic opportunities. Highlight key insights for decision-making. Audience: $AUDIO_AUDIENCE, Tone: $AUDIO_TONE"

#### Technical Documentation (`technical-doc`)
**Focus Areas:**
- System architecture and design patterns
- API specifications and interfaces
- Implementation details and code examples
- Security and performance considerations
- Deployment and operations
- Best practices and guidelines

**Audio Instructions:**
> "Explain the technical architecture and implementation approach in detail. Cover system design, key technologies, integration points, and operational considerations. Make it accessible to $AUDIO_AUDIENCE developers. Tone: $AUDIO_TONE"

#### Business Plan (`business-plan`)
**Focus Areas:**
- Executive summary and vision
- Business model and revenue streams
- Market opportunity and strategy
- Financial projections and requirements
- Team and organizational structure
- Risk analysis and mitigation

**Audio Instructions:**
> "Present a comprehensive business plan discussion. Cover the business opportunity, strategy, financial model, and execution roadmap. Emphasize key differentiators and success factors. Audience: $AUDIO_AUDIENCE, Tone: $AUDIO_TONE"

#### Competitive Intelligence (`competitive-intel`)
**Focus Areas:**
- Competitor profiles and positioning
- Product/service comparisons
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- Pricing and business models
- Market share and customer sentiment
- Strategic recommendations

**Audio Instructions:**
> "Provide an in-depth competitive intelligence briefing. Analyze key competitors, their strategies, strengths and weaknesses. Identify opportunities for differentiation and competitive advantage. Audience: $AUDIO_AUDIENCE, Tone: $AUDIO_TONE"

#### Custom Research (`custom`)
**Focus Areas:**
- User-defined research objectives
- Flexible analysis framework
- Source synthesis and insights
- Actionable recommendations

**Audio Instructions:**
> "Synthesize the research findings from all sources. Provide key insights, patterns, and actionable recommendations relevant to $PROJECT. Audience: $AUDIO_AUDIENCE, Tone: $AUDIO_TONE"

### Phase 4: Content Generation

1. **Generate Requested Outputs**
   - Parse the `output_types` parameter
   - For each requested output type:

   **If 'guide' or 'all':**
   - Run: `nlm generate-guide <notebook-id>`
   - Save output to file: `<notebook-id>_guide.md`

   **If 'outline' or 'all':**
   - Run: `nlm generate-outline <notebook-id>`
   - Save output to file: `<notebook-id>_outline.md`

   **If 'section' or 'all':**
   - Run: `nlm generate-section <notebook-id>`
   - Save output to file: `<notebook-id>_section.md`

   **If 'audio' or 'all':**
   - Run: `nlm audio-create <notebook-id> "custom-instructions"`
   - Wait for audio generation (poll status if needed)
   - Run: `nlm audio-get <notebook-id>`
   - Save transcript to: `<notebook-id>_audio_transcript.md`
   - Save share link to: `<notebook-id>_audio_link.txt`

2. **Create Index Note**
   - Run: `nlm new-note <notebook-id> "Research Index"`
   - Edit note with structured summary:
     - Project name and research type
     - Source list with descriptions
     - Key findings and insights
     - Links to generated outputs
     - Timestamp and metadata

### Phase 5: Export & Organization

1. **Organize Output Files**
   - If `save-to` is specified:
     - Create directory structure: `$SAVE_TO/$PROJECT-$TYPE-YYYYMMDD/`
     - Move all generated files to this directory
     - Create a `README.md` with:
       - Project overview
       - Source list
       - Output file descriptions
       - NotebookLM notebook link
       - Generation timestamp

2. **Summary Report**
   - Generate a final summary including:
     - Notebook ID and link
     - Number of sources added (by type)
     - Output files generated
     - Key insights (3-5 bullet points)
     - Next steps or recommendations
     - Export location

### Phase 6: Quality Assurance

1. **Verification Checklist**
   - [ ] All requested sources were added successfully
   - [ ] All requested outputs were generated
   - [ ] Files are properly organized in export directory
   - [ ] Audio transcript and share link are accessible
   - [ ] Index note contains complete information
   - [ ] Summary report is comprehensive

2. **Error Handling**
   - If sources fail to add: Log warning, continue with successful sources
   - If audio generation fails: Retry once, then skip if still failing
   - If export directory doesn't exist: Create it with proper permissions
   - If any critical error occurs: Provide clear error message with troubleshooting steps

## Output Format

Present the final results in this structure:

```markdown
# Research Complete: $PROJECT

## 📊 Research Type
$TYPE

## 📚 Sources Processed
- URLs: [count]
- Files: [count]
- Documents: [count]
- Text: [count]

## 📝 Generated Outputs
- ✓ Guide: [path or link]
- ✓ Outline: [path or link]
- ✓ Audio Overview: [share link]
- ✓ Transcript: [path]

## 💡 Key Insights
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

## 🔗 NotebookLM Access
Notebook ID: [id]
Direct Link: [notebook-url]

## 📁 Export Location
All files saved to: $SAVE_TO/$PROJECT-$TYPE-YYYYMMDD/

## ⏭️  Next Steps
[Suggested actions based on research findings]
```

## Usage Examples

### Example 1: MVP Product Design
```bash
claude nlm-research \
  --project="Acme Task Manager" \
  --type=mvp-design \
  --urls="https://notion.so,https://asana.com,https://linear.app" \
  --files="./requirements.pdf,./user-research.md" \
  --outputs="guide,outline,audio" \
  --audio-audience="technical" \
  --save-to="./research/acme-mvp"
```

### Example 2: Market Analysis
```bash
claude nlm-research \
  --project="E-commerce Beauty Market" \
  --type=market-analysis \
  --urls="https://market-report.com/beauty-2024,https://statista.com/beauty" \
  --docs="https://docs.google.com/document/d/abc123" \
  --outputs="guide,audio" \
  --audio-audience="executive" \
  --audio-tone="formal" \
  --save-to="./research/beauty-market"
```

### Example 3: Technical Documentation
```bash
claude nlm-research \
  --project="API Integration Guide" \
  --type=technical-doc \
  --files="./api-spec.yaml,./architecture.md" \
  --text="Integration requirements: OAuth2, REST API, rate limiting" \
  --outputs="guide,outline,section" \
  --save-to="./docs/api-integration"
```

### Example 4: Competitive Intelligence
```bash
claude nlm-research \
  --project="SaaS Analytics Tools" \
  --type=competitive-intel \
  --urls="https://mixpanel.com,https://amplitude.com,https://heap.io" \
  --outputs="all" \
  --audio-audience="executive" \
  --save-to="./research/competitive-analysis"
```

## Best Practices

1. **Source Quality**: Include diverse, authoritative sources for comprehensive research
2. **Rate Limiting**: Always respect NotebookLM API limits (2-5 second delays between operations)
3. **Descriptive Naming**: Use clear, searchable titles for notebooks and sources
4. **Audio Customization**: Tailor audio instructions to your specific audience and needs
5. **Export Organization**: Use consistent directory structures for easy retrieval
6. **Incremental Research**: Can run command multiple times to add sources to existing notebook
7. **Source Freshness**: For web sources, periodically refresh to capture updates

## Troubleshooting

**Authentication Errors:**
- Run `nlm auth` manually and complete OAuth flow
- Check browser for authorization popup

**Source Addition Failures:**
- Verify URLs are accessible and not behind paywalls
- Check file paths are absolute and files exist
- Ensure Google Docs have proper sharing permissions

**Audio Generation Issues:**
- Wait 30-60 seconds for processing
- Check if notebook has sufficient source content
- Try regenerating with simplified instructions

**Export Errors:**
- Verify write permissions on target directory
- Check disk space availability
- Use absolute paths instead of relative paths

## Notes

- NotebookLM has rate limits; large batches may take several minutes
- Audio generation requires substantive source content (minimum ~1000 words recommended)
- Generated content quality depends on source quality and relevance
- Notebooks persist in your NotebookLM account for future reference
- Can be combined with other commands for workflow automation
