import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
from typing import List, Dict, Any, TypedDict, Annotated, Literal
import json
import re
from langgraph.graph import StateGraph, END

# Import the new scrapers
try:
    from scraper.google_search import GoogleSearcher
    from scraper.web_browser import WebBrowser
except ImportError:
    # Handle direct execution where module path might differ
    try:
        from DeepWebResearcher.scraper.google_search import GoogleSearcher
        from DeepWebResearcher.scraper.web_browser import WebBrowser
    except ImportError:
        # Fallback for when running from the same directory
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from scraper.google_search import GoogleSearcher
        from scraper.web_browser import WebBrowser

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize custom scrapers
google_searcher = GoogleSearcher()
web_browser = WebBrowser()

# Define a Mock LLM for when keys are missing
class MockLLM:
    def __init__(self, response_text="Mocked response"):
        self.response_text = response_text

    def invoke(self, input_data):
        return self.response_text

    def __or__(self, other):
        return self

# Initialize LLMs
try:
    if OPENROUTER_API_KEY:
        from langchain_openai import ChatOpenAI
        research_llm = ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model="xiaomi/mimo-v2-flash:free",
            temperature=0.1,
            max_tokens=4000
        )

        fact_checker_llm = ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model="xiaomi/mimo-v2-flash:free",
            temperature=0.1,
            max_tokens=2000
        )
    else:
        print("Warning: OPENROUTER_API_KEY not found. Using Mock LLM.")
        research_llm = MockLLM("This is a mock research response because API keys are missing.")
        fact_checker_llm = MockLLM("This is a mock fact check response.")
except Exception as e:
    print(f"Error initializing LLMs: {e}. Using Mock LLM.")
    research_llm = MockLLM("Error initializing LLM. Mock response.")
    fact_checker_llm = MockLLM("Error initializing LLM. Mock response.")

# Initialize Tavily search with fallback
try:
    if TAVILY_API_KEY and TAVILY_API_KEY != "your_tavily_api_key_here":
        tavily_search = TavilySearchResults(api_key=TAVILY_API_KEY)
        tavily_available = True
    else:
        tavily_search = None
        tavily_available = False
        print("Warning: Tavily API key not configured. Search functionality will be limited.")
except Exception as e:
    tavily_search = None
    tavily_available = False
    print(f"Warning: Could not initialize Tavily search: {str(e)}")

def clean_json_output(text: str) -> str:
    """
    Clean LLM output to extract just the JSON part.
    Removes <think> tags, markdown code blocks, and other noise.
    """
    if not text:
        return ""

    # Remove <think> tags and content
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

    # Extract JSON from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_match:
        return json_match.group(1).strip()

    # If no code blocks, try to find the first [ or { and the last ] or }
    text = text.strip()
    if (text.startswith('[') and text.endswith(']')) or (text.startswith('{') and text.endswith('}')):
        return text

    return text

summarize_prompt = ChatPromptTemplate.from_template("""
You are a research assistant that summarizes and structures search results.

Given the following raw search results:

{search_results}

Please provide a well-structured summary that:
1. Extracts the key information
2. Organizes it in a clear, logical manner
3. Removes any redundant or irrelevant information
4. Cites sources appropriately
5. Presents a comprehensive overview of the topic

Your summary should be detailed enough to provide valuable insights on the query: {query}
""")

def summarize_search_results(query: str, search_results: List[Dict[str, Any]]) -> str:
    """Summarize and structure search results using LLM"""
    try:
        # Ensure search_results is a list
        if not isinstance(search_results, list):
            print(f"Warning: Expected list of search results, got {type(search_results)}")
            if isinstance(search_results, str):
                search_results = [{"url": "N/A", "title": "Search Result", "content": search_results}]
            else:
                search_results = []
        
        # Format search results 
        formatted_results = "\n\n".join([
            f"Source: {result.get('url', 'Unknown')}\n"
            f"Title: {result.get('title', 'No title')}\n"
            f"Content: {result.get('content', 'No content')}"
            for result in search_results
        ])
        
        if isinstance(research_llm, MockLLM):
            return f"Mock Summary for query: {query}. Found {len(search_results)} results."

        #  summarization chain
        chain = summarize_prompt | research_llm | StrOutputParser()
        return chain.invoke({"query": query, "search_results": formatted_results})
    except Exception as e:
        print(f"Error in summarize_search_results: {str(e)}")
        return f"Could not summarize search results due to an error: {str(e)}"
# Creating  custom  summarization tool 
def parse_summarize_input(input_str):
    """Parse the input for the summarize tool, handling potential JSON format issues."""
    try:
        # JSON parsing
        data = json.loads(input_str)
        return summarize_search_results(data["query"], data["results"])
    except json.JSONDecodeError:
        print(f"Failed to parse input as JSON: {input_str}")
        return "Error: Input must be a JSON string with 'query' and 'results' fields. Please format your input correctly."

summarize_tool = Tool(
    name="SummarizeResults",
    description="Summarizes and structures search results into a comprehensive research output. Input must be a JSON string with 'query' and 'results' fields.",
    func=parse_summarize_input
)

# Tavily search tool for fact verification with fallback
try:
    if TAVILY_API_KEY and TAVILY_API_KEY != "your_tavily_api_key_here":
        fact_verification_search = TavilySearchResults(
            api_key=TAVILY_API_KEY,
            max_results=5,
            search_depth="advanced"
        )
    else:
        fact_verification_search = None
        print("Warning: Tavily API key not configured for fact verification.")
except Exception as e:
    fact_verification_search = None
    print(f"Warning: Could not initialize Tavily fact verification: {str(e)}")

# Function to extract key claims from research output
def extract_claims(research_output):
    if isinstance(fact_checker_llm, MockLLM):
        return [{"claim": "Mock claim based on research.", "importance": "medium"}]

    try:
        extraction_prompt = ChatPromptTemplate.from_template("""
        You are an expert at identifying factual claims in text. 
        From the following research output, extract the 3-5 most significant factual claims that should be verified.

        Research output:
        {research_output}

        For each claim, provide:
        1. The claim statement
        2. The importance of verifying this claim (high/medium/low)

        Format your response as a JSON array of objects with "claim" and "importance" fields.
        Example:
        [
            {{"claim": "The sky is blue.", "importance": "low"}},
            {{"claim": "Water boils at 100C at sea level.", "importance": "high"}}
        ]

        IMPORTANT: Return ONLY the JSON array. Do not include markdown formatting or explanations.
        """)

        chain = extraction_prompt | fact_checker_llm | StrOutputParser()
        result_text = chain.invoke({"research_output": research_output})

        # Clean and parse JSON
        cleaned_text = clean_json_output(result_text)
        try:
            result = json.loads(cleaned_text)
        except json.JSONDecodeError:
            print(f"Failed to parse claims JSON: {cleaned_text[:100]}...")
            return [{"claim": "Error parsing claims", "importance": "low"}]
        
        # Ensure we return a list
        if not isinstance(result, list):
            print(f"Warning: Expected list of claims, got {type(result)}")
            if isinstance(result, dict) and "claim" in result:
                return [result]
            return [{"claim": "No claims could be extracted", "importance": "low"}]
            
        return result
    except Exception as e:
        print(f"Error in extract_claims: {str(e)}")
        return [{"claim": f"Error extracting claims: {str(e)}", "importance": "low"}]
# credibility check prompt
credibility_check_prompt = ChatPromptTemplate.from_template("""
You are a critical fact-checker analyzing research content. Evaluate the following claim:

CLAIM: {claim}

Based on your analysis and the provided verification data:
{verification_data}

Please provide a detailed assessment with:
1. Accuracy score (0-10)
2. Confidence level (0-10)
3. Specific inaccuracies or misrepresentations (if any)
4. Missing context or nuance
5. Potential biases in the original claim

Format your response as a JSON object with the following structure:
{{
    "accuracy_score": <score>,
    "confidence_level": <level>,
    "inaccuracies": ["<issue1>", "<issue2>", ...],
    "missing_context": ["<context1>", "<context2>", ...],
    "potential_biases": ["<bias1>", "<bias2>", ...],
    "corrected_claim": "<improved version of the claim>"
}}
""")

# Function to verify a single claim
def verify_claim(claim):
    if isinstance(fact_checker_llm, MockLLM):
        return {
            "accuracy_score": 8,
            "confidence_level": 9,
            "inaccuracies": [],
            "missing_context": ["Mock verification"],
            "potential_biases": [],
            "corrected_claim": claim
        }

    try:
        # Use our Google Searcher first as it's the "free" option
        search_results = google_searcher.search(claim, num_results=5)

        if not search_results and fact_verification_search:
            # Fallback to Tavily if Google/DDG fails and Tavily is available
            search_results = fact_verification_search.invoke(claim)
    except Exception as e:
        print(f"Search error for claim '{claim}': {e}")
        search_results = []

    verification_data = "\n\n".join([
        f"Source: {result.get('url', 'Unknown')}\n"
        f"Title: {result.get('title', 'No title')}\n"
        f"Content: {result.get('snippet', result.get('content', 'No content'))}"
        for result in search_results
    ])

    # Add explicit instruction to not include think tags
    modified_prompt = ChatPromptTemplate.from_template("""
    You are a critical fact-checker analyzing research content. Evaluate the following claim:

    CLAIM: {claim}

    Based on your analysis and the provided verification data:
    {verification_data}

    Please provide a detailed assessment with:
    1. Accuracy score (0-10)
    2. Confidence level (0-10)
    3. Specific inaccuracies or misrepresentations (if any)
    4. Missing context or nuance
    5. Potential biases in the original claim

    Format your response as a JSON object with the following structure:
    {{
        "accuracy_score": <score>,
        "confidence_level": <level>,
        "inaccuracies": ["<issue1>", "<issue2>", ...],
        "missing_context": ["<context1>", "<context2>", ...],
        "potential_biases": ["<bias1>", "<bias2>", ...],
        "corrected_claim": "<improved version of the claim>"
    }}

    IMPORTANT: Do not include any <think> or </think> tags in your response. Provide only valid JSON.
    """)

    try:
        chain = modified_prompt | fact_checker_llm | StrOutputParser()
        result_text = chain.invoke({"claim": claim, "verification_data": verification_data})

        # Clean and parse
        cleaned_text = clean_json_output(result_text)
        result = json.loads(cleaned_text)
        return result
    except Exception as e:
        print(f"Error parsing fact-check response: {str(e)}")
        # Fallback response if parsing fails
        return {
            "accuracy_score": 5,
            "confidence_level": 5,
            "inaccuracies": [f"Could not properly verify: {str(e)}"],
            "missing_context": ["Verification process failed"],
            "potential_biases": ["Unable to assess due to verification failure"],
            "corrected_claim": claim
        }
# Function to extract references from verification data
def extract_references(verification_results):
    references = []
    for i, result in enumerate(verification_results, 1):
        verification_data = result.get("verification_data", "")
        # Try to find Source patterns
        sources = re.findall(r"Source: (https?://[^\n]+)", verification_data)
        for source in sources:
            if source not in [ref.split(". ")[1] for ref in references]:
                references.append(f"{len(references) + 1}. {source}")
    return references

# query optimization function
def optimize_query_directly(query: str) -> str:
    if isinstance(research_llm, MockLLM):
        return query

    optimization_prompt = ChatPromptTemplate.from_template("""
    You are a query optimization expert. Your task is to transform the user's query into a
    concise, effective search string suitable for a standard search engine.

    Original query: {query}

    Please provide an optimized version of this query that:
    1. Removes conversational language (e.g., "tell me about", "what is")
    2. Focuses on key concepts and domain terminology
    3. Is a simple string (no boolean operators like AND/OR/NOT unless absolutely necessary)
    4. Is short enough to be processed by standard search APIs

    IMPORTANT: Return ONLY the optimized query string. Do not include any explanations, labels, or markdown formatting.
    Just the query text itself.
    """)
    
    chain = optimization_prompt | research_llm | StrOutputParser()
    result = chain.invoke({"query": query})

    # Clean up any potential leftover artifacts
    cleaned_result = clean_json_output(result)
    # Remove common prefixes if they still appear
    cleaned_result = re.sub(r'^(Optimized query:|Query:|Here is the optimized query:)\s*', '', cleaned_result, flags=re.IGNORECASE).strip()
    # Remove quotes if the entire string is quoted
    if (cleaned_result.startswith('"') and cleaned_result.endswith('"')) or (cleaned_result.startswith("'") and cleaned_result.endswith("'")):
        cleaned_result = cleaned_result[1:-1]

    return cleaned_result

#  content style selection functions
def select_content_style(style_number: int) -> str:
    styles = {1: "blog post", 2: "detailed report", 3: "executive summary", 4: "latex detailed report", 5: "latex executive summary"}
    return styles.get(style_number, "blog post")  # Default to blog post if invalid number

def get_style_prompt(style: str) -> str:
    if style == "blog post":
        return "Create an engaging blog post that presents the research findings in a conversational tone with clear headings, examples, and actionable insights."
    elif style == "detailed report":
        return "Structure a comprehensive report with executive summary, methodology, findings, analysis, and recommendations. Include relevant data points and cite sources appropriately."
    elif style == "executive summary":
        return "Provide a concise executive summary highlighting key findings, implications, and recommended actions. Focus on business impact and strategic considerations."
    elif style == "latex detailed report":
        return """Create a comprehensive LaTeX-style detailed report with the following structure:

# Title: [Research Topic] - A Comprehensive Analysis

## Abstract
Provide a concise summary of the research objectives, methodology, key findings, and implications.

## 1. Introduction
### 1.1 Background
Provide context and historical developments related to the research topic.

### 1.2 Problem Statement
Clearly define the primary issues and challenges addressed in this research.

### 1.3 Research Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## 2. Methodology
### 2.1 Research Design
Describe the approach and methodology used in this research.

### 2.2 Data Collection
Detail the sources and methods of data collection.

### 2.3 Data Analysis
Explain the analytical methods and tools used.

## 3. Results and Findings
### 3.1 Key Findings
Present the main research findings with supporting data.

### 3.2 Analysis
Provide detailed analysis of the findings and their implications.

### 3.3 Data Visualization
Include relevant tables, charts, and visual representations where appropriate.

## 4. Discussion
### 4.1 Interpretation of Results
Analyze and interpret the research findings in context.

### 4.2 Implications
Discuss the broader implications of the findings.

### 4.3 Limitations
Acknowledge any limitations of the research methodology or findings.

## 5. Conclusion and Recommendations
### 5.1 Summary
Summarize the key findings and their significance.

### 5.2 Recommendations
Provide actionable recommendations based on the research findings.

## References
List all sources and references used in the research.

Use professional academic writing style with proper citations, clear structure, and comprehensive coverage of the topic."""
    elif style == "latex executive summary":
        return """Create a professional LaTeX-style executive summary with the following structure:

# Executive Summary: [Research Topic]

## Executive Summary

Provide a concise overview of the project's objectives, methodologies, key findings, and recommendations. Focus on high-level insights and strategic implications.

## Objectives
Clearly state the primary goals and objectives of the research project.

## Methodology
Briefly describe the approach and methods used in the research.

## Key Findings
Present the most important findings with supporting data and metrics.

## Recommendations
Provide actionable recommendations based on the research findings.

## Conclusion
Summarize the overall impact and next steps.

Use professional business writing style with clear, concise language suitable for executive audiences. Focus on strategic insights and actionable outcomes."""

#states for the LangGraph workflow
class ResearchState(TypedDict):
    query: str
    optimized_query: str
    research_output: str
    claims: List[Dict[str, Any]]
    verification_results: List[Dict[str, Any]]
    references: List[str]
    fact_check_report: str
    content_style: str
    draft_content: str
    status: str

#nodes for the LangGraph workflow
def optimize_query(state: ResearchState) -> ResearchState:
    print("Optimizing query...")
    optimized_query = optimize_query_directly(state["query"])
    return {"optimized_query": optimized_query}

def conduct_research(state: ResearchState) -> ResearchState:
    print(f"Conducting research on: {state['optimized_query']}")
    
    # Check if this is a direct URL scraping request
    is_url = re.match(r'https?://[^\s]+', state['query'].strip())
    
    research_results = []
    
    try:
        if is_url:
            print(f"Detected URL. Using WebBrowser to scrape: {state['query']}")
            content = web_browser.scrape_url(state['query'])
            research_results = [{
                "url": state['query'],
                "title": "Direct URL Scrape",
                "content": content,
                "source": "Web Browser"
            }]
        else:
            # Smart Routing Logic
            print(f"Using Google Searcher for query: {state['optimized_query']}")
            
            # Step 1: Get Google/DDG Results
            search_results = google_searcher.search(state["optimized_query"], num_results=10)
            
            # Step 2: For "Deep Research", we want to actually visit the top links
            # Let's say we pick the top 3 organic results to deep-scrape
            print("Deep scraping top 3 results...")

            research_results = []

            # Add snippets first (fast context)
            for res in search_results:
                research_results.append({
                    "url": res['url'],
                    "title": res['title'],
                    "content": res['snippet'],
                    "source": res['source'] + " (Snippet)"
                })

            # Then deep scrape the top 3
            count = 0
            for res in search_results:
                if count >= 3:
                    break

                if "DuckDuckGo" in res['source'] or "Google" in res['source']:
                    print(f"Deep scraping: {res['url']}")
                    content = web_browser.scrape_url(res['url'])

                    if content and not content.startswith("Error"):
                         research_results.append({
                            "url": res['url'],
                            "title": res['title'],
                            "content": content[:8000], # Limit content length for context window
                            "source": "Web Browser Scraper"
                        })
                    count += 1

            if not research_results and tavily_available:
                print("Primary search yielded no results. Falling back to Tavily...")
                search_results = tavily_search.invoke(state["optimized_query"])
                research_results = search_results

        # Summarize the combined results
        research_output = summarize_search_results(state["optimized_query"], research_results)
        return {"research_output": research_output}

    except Exception as e:
        print(f"Error in conduct_research: {str(e)}")
        return {"research_output": f"Research could not be completed due to an error: {str(e)}"}

def extract_key_claims(state: ResearchState) -> ResearchState:
    print("Extracting key claims from research output...")
    claims = extract_claims(state["research_output"])
    return {"claims": claims}

def verify_claims(state: ResearchState) -> ResearchState:
    print("Verifying claims against trusted sources...")
    verification_results = []
    
    # Handle case where claims might be a string or invalid format
    claims = state["claims"]
    if not isinstance(claims, list):
        print(f"Warning: Expected list of claims, got {type(claims)}")
        claims = [{"claim": "No claims to verify", "importance": "low"}]
    
    for claim_item in claims:
        if not isinstance(claim_item, dict):
            print(f"Warning: Expected dict for claim item, got {type(claim_item)}")
            continue
            
        claim = claim_item.get("claim", "No claim provided")
        importance = claim_item.get("importance", "low")
        
        try:
            # Use our verification logic (Google/DDG -> Tavily fallback)
            verification = verify_claim(claim)

            # For data collection, we re-run the search to get the snippets for the record
            # (verify_claim does this internally but returns the analysis)
            # We reconstruct the "verification_data" for the report

            search_results = google_searcher.search(claim, num_results=5)
            if not search_results and fact_verification_search:
                 search_results = fact_verification_search.invoke(claim)

            verification_data = "\n\n".join([
                f"Source: {result.get('url', 'Unknown')}\n"
                f"Title: {result.get('title', 'No title')}\n"
                f"Content: {result.get('snippet', result.get('content', 'No content'))}"
                for result in search_results
            ])
            
            verification["claim"] = claim
            verification["importance"] = importance
            verification["verification_data"] = verification_data
            verification_results.append(verification)
        except Exception as e:
            print(f"Error verifying claim '{claim}': {str(e)}")
            verification_results.append({
                "claim": claim,
                "importance": importance,
                "verification_data": f"Error during verification: {str(e)}",
                "accuracy_score": 0,
                "confidence_level": 0,
                "inaccuracies": ["Verification failed"],
                "missing_context": [],
                "potential_biases": [],
                "corrected_claim": claim
            })
    
    # Extract references from verification data
    references = extract_references(verification_results)
    
    return {
        "verification_results": verification_results,
        "references": references
    }

def generate_fact_check_report(state: ResearchState) -> ResearchState:
    print("Generating fact-check report...")
    if isinstance(fact_checker_llm, MockLLM):
        return {"fact_check_report": "Mock Fact Check Report: Research appears valid."}

    # Clean verification results for the prompt by removing verification_data
    clean_verification_results = []
    for v in state["verification_results"]:
        v_clean = v.copy()
        if "verification_data" in v_clean:
            del v_clean["verification_data"]
        clean_verification_results.append(v_clean)
    
    overall_report_prompt = ChatPromptTemplate.from_template("""
    You are a critical fact-checker generating a comprehensive verification report.
    
    Original research output:
    {research_output}
    
    Detailed verification results for key claims:
    {verification_results}
    
    References used in verification:
    {references}
    
    Please provide a comprehensive fact-check report that:
    1. Summarizes the overall reliability of the research (with an overall score from 0-10)
    2. Highlights the most significant accuracy issues
    3. Provides context for any misleading or incomplete information
    4. Suggests improvements to make the research more accurate and balanced
    5. Includes a properly formatted "References" section at the end listing all sources used in verification
    
    Your report should be detailed, fair, and constructive. Make sure to cite specific references by number when discussing claims.
    """)
    
    chain = overall_report_prompt | fact_checker_llm | StrOutputParser()
    fact_check_report = chain.invoke({
        "research_output": state["research_output"],
        "verification_results": json.dumps(clean_verification_results, indent=2),
        "references": "\n".join(state["references"])
    })
    
    return {"fact_check_report": fact_check_report}

def create_draft_content(state: ResearchState) -> ResearchState:
    print(f"Drafting content in {state['content_style']} style...")
    
    if isinstance(research_llm, MockLLM):
        return {
            "draft_content": f"Mock Draft Content for query '{state['optimized_query']}' in style '{state['content_style']}'.\n\nThis is a placeholder draft since no API keys were provided.",
            "status": "completed"
        }

    draft_prompt = ChatPromptTemplate.from_template("""
    Based on the comprehensive research results, create a high-quality {style} content about the query: {optimized_query}
    
    Research findings: {research}
    Fact-check report: {fact_check}
    References: {references}
    
    Your task is to create engaging, informative content that:
    
    1. **Focuses on the core topic** - Address the query directly with detailed, relevant information
    2. **Uses the research findings** - Incorporate the comprehensive research data and insights
    3. **Maintains accuracy** - Consider the fact-check report to ensure information is reliable
    4. **Provides value** - Deliver actionable insights, practical examples, and useful information
    5. **Engages the audience** - Use clear, compelling writing that holds reader interest
    6. **Includes proper references** - Cite sources appropriately at the end
    
    Content requirements:
    - Write in a {style} format appropriate for the target audience
    - Include specific examples, case studies, or practical applications
    - Provide technical details when relevant
    - Address common questions or concerns about the topic
    - Offer actionable advice or recommendations
    - Use clear, professional language
    - Structure content logically with proper headings and sections
    
    Do not include any <think> or </think> tags in your response.
    Focus on delivering substantial, valuable content that provides real insights and practical value to readers.
    """)
    
    chain = draft_prompt | research_llm | StrOutputParser()
    draft_content = chain.invoke({
        "optimized_query": state["optimized_query"],
        "research": state["research_output"],
        "fact_check": state["fact_check_report"],
        "style": state["content_style"],
        "references": "\n".join(state["references"])
    })
    draft_content = re.sub(r'<think>.*?</think>', '', draft_content, flags=re.DOTALL)
    
    return {
        "draft_content": draft_content,
        "status": "completed"
    }

def create_research_workflow():
    # Initialize the graph
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("optimize_query", optimize_query)
    workflow.add_node("conduct_research", conduct_research)
    workflow.add_node("extract_key_claims", extract_key_claims)
    workflow.add_node("verify_claims", verify_claims)
    workflow.add_node("generate_fact_check_report", generate_fact_check_report)
    workflow.add_node("create_draft_content", create_draft_content)
    
    # Define edges
    workflow.set_entry_point("optimize_query")
    workflow.add_edge("optimize_query", "conduct_research")
    workflow.add_edge("conduct_research", "extract_key_claims")
    workflow.add_edge("extract_key_claims", "verify_claims")
    workflow.add_edge("verify_claims", "generate_fact_check_report")
    workflow.add_edge("generate_fact_check_report", "create_draft_content")
    workflow.add_edge("create_draft_content", END)
    
    return workflow.compile()
# Main research flow function using LangGraph
def conduct_research_workflow(query: str, content_style: str) -> Dict[str, Any]:
    """
    Conduct research based on a query using the LangGraph workflow
    
    Args:
        query: The user's original query
        content_style: Desired content style for the draft
        
    Returns:
        Dictionary containing all research results and content draft
    """
    print(f"Starting research workflow on query: {query}")
    
    try:
        workflow = create_research_workflow()
        
        initial_state = {
            "query": query,
            "optimized_query": "",
            "research_output": "",
            "claims": [],
            "verification_results": [],
            "references": [],
            "fact_check_report": "",
            "content_style": content_style,
            "draft_content": "",
            "status": "in_progress"
        }
        
        result = workflow.invoke(initial_state)
        
        return result
    except Exception as e:
        print(f"Error in research workflow: {str(e)}")
        return {
            "query": query,
            "optimized_query": "",
            "research_output": f"Error during research: {str(e)}",
            "fact_check_report": "Fact-checking could not be performed due to research error.",
            "content_style": content_style,
            "draft_content": "",
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    ####### this input output is for testing purposes onlyin ternimal  
    user_query = input("Enter your research query: ")
    
    print("\nSelect content style:")
    print("1. Blog post")
    print("2. Detailed report")
    print("3. Executive summary")
    style_number = int(input("Enter style number (1-3): "))
    content_style = select_content_style(style_number)
    print(f"Selected style: {content_style}")
    
    # Execute the research workflow
    result = conduct_research_workflow(user_query, content_style)
    
    # Display results
    print("\n" + "="*50)
    print("RESEARCH WORKFLOW RESULTS")
    print("="*50)
    
    if result.get("status") == "completed":
        print(f"Original Query: {result['query']}")
        print(f"Optimized Query: {result['optimized_query']}")
        
        print("\nRESEARCH OUTPUT:")
        print("-"*50)
        print(result['research_output'])
        
        print("\nFACT-CHECK REPORT:")
        print("-"*50)
        print(result['fact_check_report'])
        
        print("\nCONTENT DRAFT:")
        print("-"*50)
        print(f"Style: {result['content_style']}")
        print(result['draft_content'])
    else:
        print(f"Workflow Error: {result.get('error', 'Unknown error')}")
        print("Partial results:")
        for key, value in result.items():
            if key not in ["error", "status"] and value:
                print(f"\n{key.upper()}:")
                print(value)
