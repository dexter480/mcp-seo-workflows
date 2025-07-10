# Article SEO Optimization Workflow
## Using MCP Tools for Keywords Everywhere and SERP API

### Overview
This workflow takes an article structure, analyzes it to understand the core topic, performs keyword research and SERP analysis, then suggests optimizations to align with search intent and keyword opportunities.

---

## Step 1: Article Structure Analysis

### User Input Required:
- Article title/topic
- Heading structure (H1, H2, H3, etc.)
- Brief content outline (optional)
- Target audience (optional)

### AI Analysis Process:
The AI will analyze the provided structure to extract:

**Core Topic Identification:**
- Primary subject matter
- Main theme and focus
- Content angle and approach

**Content Intent Analysis:**
- Article purpose (educational, commercial, informational)
- Target audience level (beginner, intermediate, advanced)
- Content type (how-to, listicle, comparison, guide, etc.)

**Topic Extraction:**
- Main keywords from headings
- Secondary topics covered
- Related themes and concepts

---

## Step 2: Keyword Research & Semantic Topic Discovery

### 2.1 Semantic Topic Analysis

**Topic Entity Extraction:**
- Identify core entities and concepts from article structure
- Extract semantic themes and subject clusters
- Map relationships between topics and subtopics
- Understand topical authority context

**Semantic Keyword Groups:**
- Primary topic cluster (main theme)
- Supporting topic clusters (subtopics)
- Related concept clusters (adjacent topics)
- Long-tail semantic variations

### 2.2 Related Keywords Discovery
```
Tool: seo-scraper:related_keywords_discovery
Parameters:
- keyword: [main topic extracted from article]
- country: "US"
- api_key: [Keywords Everywhere API key]
```

**Process:**
- Extract 3-5 seed keywords from semantic analysis
- Discover related keywords for each topic cluster
- Identify semantic keyword relationships
- Categorize by search intent and topical relevance

### 2.3 Comprehensive Keyword Research Analysis
```
Tool: seo-scraper:keyword_research_analysis
Parameters:
- keywords: [list from discovery + semantic extraction]
- country: "US" 
- api_key: [Keywords Everywhere API key]
```

**Analysis Focus:**
- Search volume data across topic clusters
- Competition levels for semantic groups
- Cost-per-click insights by topic theme
- Keyword difficulty scores by semantic cluster

### 2.4 Semantic Opportunity Scoring
```
Tool: seo-scraper:keyword_opportunity_scorer
Parameters:
- keywords: [filtered semantic keyword list]
- business_relevance_keywords: [topic cluster terms]
- country: "US"
- api_key: [Keywords Everywhere API key]
```

**Scoring Criteria:**
- Volume vs. competition ratio within topic clusters
- Semantic relevance to core article theme
- Topic authority building potential
- Topical coverage completeness
- Ranking difficulty by semantic group

---

## Step 3: SERP Analysis & Semantic Intent Classification

### 3.1 Search Intent & Semantic Classification
```
Tool: seo-scraper:classify_search_intent_data
Parameters:
- keyword: [primary target keyword]
- api_key: [SerpAPI key]
- location: "United States"
```

**Intent Types & Semantic Context:**
- **Informational**: How-to guides, explanations, tutorials + related learning topics
- **Commercial**: Reviews, comparisons, "best of" lists + evaluation criteria topics
- **Transactional**: Purchase-focused, pricing content + decision-making factors
- **Navigational**: Brand or specific site searches + brand-related topics

**Semantic Search Patterns:**
- Topic clusters present in SERP results
- Related concepts Google associates with the keyword
- Semantic entities appearing across top results
- Topic depth and coverage expectations

### 3.2 SERP Feature & Topic Opportunities
```
Tool: seo-scraper:analyze_serp_feature_opportunities
Parameters:
- keyword: [target keyword]
- target_url: [existing URL if available]
- api_key: [SerpAPI key] 
- location: "United States"
```

**SERP Features Analysis:**
- Featured snippets opportunities + required semantic coverage
- People Also Ask questions + related topic themes
- Related searches + semantic keyword clusters
- Image pack potential + visual topic associations
- Video results presence + multimedia topic angles

**Semantic Content Patterns:**
- Topic breadth in featured snippets
- Semantic themes in PAA questions
- Related concept coverage in top results
- Entity associations across SERP features

### 3.3 Content & Semantic Alignment Analysis  
```
Tool: seo-scraper:analyze_serp_content_alignment
Parameters:
- keyword: [primary keyword]
- target_url: [article URL if exists]
- api_key: [SerpAPI key]
- location: "United States"
```

**Competitive Semantic Analysis:**
- Topic clusters covered by top-ranking content
- Semantic keyword density and distribution
- Related concept integration patterns
- Content depth across semantic themes
- Topical authority signals in top results

**Content Gaps & Semantic Opportunities:**
- Missing topic clusters in current content
- Under-covered semantic themes
- Related concepts not addressed
- Semantic keyword integration opportunities

---

## Step 4: Article Optimization Recommendations

### 4.1 Semantic Content Structure Alignment

**Title Optimization:**
- Integrate primary keyword naturally
- Include semantic signals (how-to, best, guide, etc.)
- Reflect core topic cluster theme
- Optimize for click-through rate and topical relevance

**Heading Structure Refinement:**
- Organize H2/H3 around semantic topic clusters
- Include secondary keywords from related topic groups
- Add sections covering semantic themes found in SERP analysis
- Structure for featured snippet opportunities with topic depth
- Map headings to semantic keyword clusters

**Content Sections to Add (Semantic-Driven):**
- FAQ section targeting PAA semantic themes
- Topic clusters identified in competitive analysis
- Related concept coverage gaps
- Semantic entity explanations and context
- Supporting topic clusters for topical authority

### 4.2 Keyword Integration & Semantic Strategy

**Primary Keyword Placement:**
- H1 (title) - natural integration with semantic context
- First paragraph - within first 100 words with related concepts
- H2 subheadings - where topically relevant with semantic support
- Throughout content - maintain natural semantic flow

**Semantic Keyword Distribution:**
- Distribute topic clusters across content sections
- Integrate related entities and concepts naturally
- Use semantic keyword variations and synonyms
- Include long-tail semantic phrases
- Build topical keyword clusters throughout content

**Entity & Concept Integration:**
- Include related entities identified in semantic analysis
- Connect concepts through natural semantic relationships
- Use co-occurring terms found in top-ranking content
- Build semantic bridges between topic clusters

### 4.3 Search Intent & Semantic Optimization

**Match Content Format to Intent + Topics:**
- **Informational**: Step-by-step guides with comprehensive topic coverage
- **Commercial**: Comparisons with related decision-factor topics  
- **Transactional**: Clear CTAs with supporting semantic context

**Semantic Content Depth Adjustments:**
- Expand topic clusters based on semantic analysis
- Add related concept explanations and context
- Include expert insights on semantic themes
- Address user questions across topic clusters comprehensively
- Build topical authority through comprehensive coverage

### 4.4 SERP Feature & Semantic Optimization

**Featured Snippet Targeting:**
- Format content around semantic topic clusters
- Use numbered lists, bullet points for topic organization
- Provide direct answers with semantic context
- Structure content with clear topic hierarchy

**People Also Ask & Semantic Integration:**
- Add FAQ section with semantic theme questions
- Answer related queries within topic clusters
- Use question-based H2/H3 with semantic keywords
- Provide comprehensive answers across related topics

**Topic Cluster Organization:**
- Group related concepts into logical sections
- Create semantic content hubs within the article
- Link related topics through natural transitions
- Build comprehensive topic coverage for authority

---

## Step 5: Implementation Recommendations

### Content Changes:
- [ ] Update title with primary keyword
- [ ] Restructure headings based on SERP insights
- [ ] Add missing content sections identified
- [ ] Integrate keywords naturally throughout
- [ ] Create FAQ section for PAA opportunities
- [ ] Optimize content length to match competitors

### Optimization Priorities:
- [ ] Align content with identified search intent
- [ ] Target highest-opportunity keywords first
- [ ] Format content for featured snippets
- [ ] Address content gaps vs. competitors
- [ ] Maintain natural, user-focused writing

---

## Example Workflow Execution

### Sample Input:
```
Article Structure:
H1: "How to Start a Home Garden"
H2: "Choosing Your Garden Location"  
H2: "Essential Gardening Tools"
H2: "Best Plants for Beginners"
H2: "Watering and Care Tips"
```

### AI Semantic Analysis:
1. **Topic Analysis**: Beginner gardening guide, informational intent
2. **Semantic Topic Clusters Identified**:
   - **Core Cluster**: Garden planning and setup
   - **Supporting Clusters**: Plant selection, tool requirements, maintenance routines
   - **Related Concepts**: Soil preparation, seasonal timing, garden types, space planning
   - **Entity Associations**: Indoor/outdoor gardens, container gardening, raised beds

3. **Keyword Research with Semantic Context**: 
   - Primary: "how to start a garden" (core cluster)
   - Semantic variations: "beginner garden setup," "garden planning guide"
   - Related clusters: "container gardening," "indoor gardening," "raised bed gardens"
   - Supporting topics: "garden soil preparation," "when to plant," "garden layout design"

4. **SERP Semantic Analysis**: 
   - Top content covers seasonal timing (missing topic cluster)
   - Budget considerations frequently mentioned (semantic theme)
   - Garden types (container, raised bed, in-ground) semantically related
   - Common mistakes topic cluster appears in PAA questions

5. **Semantic-Driven Recommendations**: 
   **Add H2 sections for topic clusters:**
   - "Planning Your Garden Layout" (space planning cluster)
   - "When to Start Your Garden" (seasonal timing cluster)  
   - "Garden Types: Container vs. In-Ground" (garden types cluster)
   - "Budget-Friendly Garden Setup" (budget considerations cluster)
   - "Common Beginner Mistakes to Avoid" (problem prevention cluster)
   
   **Integrate semantic keywords:**
   - Include "raised bed gardening" in tools section
   - Add "seasonal planting guide" concepts
   - Incorporate "small space gardening" semantic variations
   - Connect "soil preparation" throughout multiple sections

---

## API Requirements

**Keywords Everywhere API:**
- Free account: 100 searches/month
- Sign up: keywordseverywhere.com
- Get API key from dashboard

**SerpAPI:**  
- Free account: 100 searches/month
- Sign up: serpapi.com
- Get API key from dashboard

---

*This workflow provides a focused approach to optimizing article content for search performance through systematic keyword research and SERP analysis.*