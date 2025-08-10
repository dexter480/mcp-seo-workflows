# SEO Onpage Workflows for Claude 

Two SEO analysis workflows using MCP (Model Context Protocol) tools. Copy-paste these workflows into Claude to perform professional SEO analysis.

## What This Includes

- **MCP Server**: Complete SEO analysis toolset with 15+ specialized tools
- **Workflow 1**: Deep Content Optimization Intelligence (transform underperforming content)
- **Workflow 2**: Article SEO Optimization (structure-based keyword research)

## Quick Setup

### 1. Install the MCP Server
```bash
git clone https://github.com/dexter480/mcp-seo-workflows
cd seo-workflows-claude
pip install -r requirements.txt
```

### 2. Get Free API Keys
- **Keywords Everywhere**: [keywordseverywhere.com](https://keywordseverywhere.com) (100 searches/month free)
- **SerpAPI**: [serpapi.com](https://serpapi.com) (100 searches/month free)  
- **Google PageSpeed**: [developers.google.com](https://developers.google.com/speed/docs/insights/v5/get-started) (25k requests/day free)

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys:
# KEYWORDS_EVERYWHERE_API_KEY=your_key_here
# SERPAPI_KEY=your_key_here
# GOOGLE_PAGESPEED_KEY=your_key_here
```

### 4. Add to Claude Desktop

**Find your Claude config file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "seo-analyzer": {
      "command": "python",
      "args": ["/full/path/to/your/seo_scraper_mcp.py"]
    }
  }
}
```

**Replace `/full/path/to/your/` with the actual absolute path to the file.**

### 5. Test Setup
Restart Claude Desktop, then try:
```
Use the scrape_seo_data tool to analyze https://google.com
```

If you get SEO data back, you're ready to use the workflows!

## Available Workflows

### 🔬 [Deep Content Optimization](workflows/content-optimization.md)
**Transform underperforming content into top-ranking pages**

- Systematic content analysis using the SEMANTIC method
- Competitive landscape & intent analysis  
- NLP & content quality optimization
- Comprehensive optimization strategy with implementation roadmap

**Best for**: Optimizing existing blog posts, landing pages, product pages
**Time**: 1-2 hours per page
**Tools used**: All content analysis, SERP intelligence, and keyword research tools

### 📝 [Article SEO Optimization](workflows/article-seo-optimization.md)
**Structure-based keyword research and SERP optimization**

- Article structure analysis and semantic topic discovery
- SERP analysis & search intent classification  
- Content alignment and optimization recommendations
- Implementation roadmap with specific action items

**Best for**: Blog posts, content marketing, new content creation
**Time**: 45-60 minutes per article
**Tools used**: Keyword research, SERP analysis, and content optimization tools

## How to Use the Workflows

1. **Choose a workflow** based on your SEO needs
2. **Open the workflow file** (in the `workflows/` folder)
3. **Copy the prompts** from the workflow into Claude
4. **Replace placeholder URLs/keywords** with your actual data
5. **Follow the step-by-step process** outlined in each workflow

Each workflow provides:
- ✅ Step-by-step prompts to copy-paste into Claude
- ✅ Specific MCP tools used in sequence  
- ✅ Expected deliverables and outcomes
- ✅ Implementation guidance and timelines

## Available MCP Tools

The workflows use these SEO analysis tools:

**Technical SEO Analysis:**
- `scrape_seo_data(url)` - Complete page SEO audit
- `page_speed_metrics(url, device)` - Core Web Vitals analysis  
- `validate_structured_data(url)` - Schema markup validation
- `collect_server_headers(url)` - Server configuration analysis
- `analyze_redirect_chain(url)` - Redirect analysis
- `detect_javascript_rendering(url)` - JS rendering detection

**SERP Intelligence:**
- `serp_data_collector(keyword)` - SERP features and rankings
- `classify_search_intent_data(keyword)` - Intent classification
- `analyze_serp_content_alignment(keyword, url)` - Content vs competitors
- `analyze_serp_feature_opportunities(keyword, url)` - SERP feature gaps

**Keyword Research:**
- `keyword_research_analysis(keywords, country)` - Volume and competition data
- `related_keywords_discovery(keyword, country)` - Related keyword discovery
- `keyword_opportunity_scorer(keywords, country)` - Opportunity scoring
- `competitor_keyword_gap_analysis(current_keywords, topics)` - Gap analysis

## Example Usage

### Quick Content Audit
```
I want to optimize my underperforming blog post: https://myblog.com/marketing-tips

Use the Deep Content Optimization workflow:
1. First, analyze the current state with scrape_seo_data
2. Then run SERP analysis for the main keyword
3. Find keyword expansion opportunities
4. Compare against top competitors
5. Provide specific optimization recommendations
```

### New Article Planning
```
I'm writing an article about "email marketing automation"

Use the Article SEO Optimization workflow:
1. Research keywords around this topic
2. Analyze search intent and SERP landscape
3. Recommend article structure and headings
4. Provide keyword integration strategy
5. Optimize for SERP features
```

### Competitor Analysis
```
Analyze how my page compares to competitors for "project management tools"

Process:
1. analyze_serp_content_alignment("project management tools", "https://mysite.com/tools")
2. analyze_serp_feature_opportunities("project management tools", "https://mysite.com/tools")

What content gaps should I address?
```

## Troubleshooting

**"API key not found" errors:**
- Ensure your `.env` file is in the same directory as `seo_scraper_mcp.py`
- Verify your API keys work by testing them on the respective platforms
- Check for typos in variable names

**"Tool not found" errors:**
- Verify the path in `claude_desktop_config.json` is absolute and correct
- Restart Claude Desktop after making configuration changes
- Test that `python /path/to/seo_scraper_mcp.py` runs without errors

**Tools timeout or fail:**
- Some analysis can take 30+ seconds for complex sites
- Ensure stable internet connection
- Check API rate limits if getting frequent errors
- Try smaller keyword lists if bulk operations fail

**Path issues on Windows:**
- Use forward slashes `/` or double backslashes `\\` in the config file
- Example: `"C:/Users/YourName/Documents/seo-workflows/seo_scraper_mcp.py"`

## What You Get

After running the workflows, you'll have:

**From Content Optimization Workflow:**
- ✅ Complete technical and content audit
- ✅ Competitive analysis vs top-ranking pages
- ✅ 8-12 related keywords with integration strategy
- ✅ Content gap analysis and expansion recommendations
- ✅ SERP feature optimization opportunities
- ✅ Week-by-week implementation roadmap

**From Article SEO Workflow:**
- ✅ Semantic keyword research and topic clusters
- ✅ Search intent analysis and content format recommendations
- ✅ Optimized article structure with strategic heading placement
- ✅ SERP feature targeting strategy
- ✅ Step-by-step content creation checklist

## Contributing

Found these workflows useful? Feel free to:
- Report issues or bugs
- Suggest workflow improvements
- Share your optimization results
- Contribute additional analysis techniques

## Acknowledgments

Built with:
- [FastMCP](https://github.com/ktanaka101/fastmcp) - MCP server framework
- [Keywords Everywhere API](https://keywordseverywhere.com) - Keyword research data
- [SerpAPI](https://serpapi.com) - Search results data  
- [Google PageSpeed API](https://developers.google.com/speed/docs/insights/v5/get-started) - Performance metrics
