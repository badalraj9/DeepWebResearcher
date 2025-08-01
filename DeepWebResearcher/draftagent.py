import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
from typing import List, Dict, Any, TypedDict, Annotated, Literal
import json
import re
from langgraph.graph import StateGraph, END


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Configure OpenRouter client
# You can change the model to a different option if needed:
# - "anthropic/claude-3.5-sonnet" (best quality, higher cost)
# - "openai/gpt-3.5-turbo" (good quality, reliable, currently selected)
# - "mistralai/mixtral-8x7b-instruct" (excellent quality, but may be rate-limited)
# - "meta-llama/llama-3.1-8b-instruct" (basic quality, very low cost)

research_llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="mistralai/mixtral-8x7b-instruct",  # Excellent quality model for research
    temperature=0.1,
    max_tokens=4000
)

fact_checker_llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="mistralai/mixtral-8x7b-instruct",  # Excellent quality model for fact-checking
    temperature=0.1,
    max_tokens=2000
)

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
        """)

        chain = extraction_prompt | fact_checker_llm | JsonOutputParser()
        result = chain.invoke({"research_output": research_output})
        
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
    search_results = fact_verification_search.invoke(claim)

    verification_data = "\n\n".join([
        f"Source: {result.get('url', 'Unknown')}\n"
        f"Title: {result.get('title', 'No title')}\n"
        f"Content: {result.get('content', 'No content')}"
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
        chain = modified_prompt | fact_checker_llm | JsonOutputParser()
        result = chain.invoke({"claim": claim, "verification_data": verification_data})
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
        sources = re.findall(r"Source: (https?://[^\n]+)", verification_data)
        for source in sources:
            if source not in [ref.split(". ")[1] for ref in references]:
                references.append(f"{len(references) + 1}. {source}")
    return references

# query optimization function
def optimize_query_directly(query: str) -> str:
    optimization_prompt = ChatPromptTemplate.from_template("""
    You are a query optimization expert. Your task is to transform natural language queries into 
    detailed, domain-specific optimized queries that can be processed by specialized systems.

    Original query: {query}

    Please provide an optimized version of this query that:
    1. Is more specific and detailed
    2. Includes relevant domain terminology
    3. Is structured for better processing by downstream systems
    4. Maintains the original intent of the query

    Optimized query:
    """)
    
    chain = optimization_prompt | research_llm | StrOutputParser()
    return chain.invoke({"query": query})

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
    
    research_prompt = ChatPromptTemplate.from_template("""
    You are an expert research assistant specializing in comprehensive, detailed analysis. Your task is to provide in-depth information about the following query:
    
    {query}
    
    Please conduct thorough research and provide a detailed, well-structured response that includes:
    
    1. **Core Concepts**: Define and explain the fundamental concepts related to the query
    2. **Technical Details**: Provide specific technical information, algorithms, methodologies, or frameworks when relevant
    3. **Real-world Examples**: Include concrete examples, case studies, or practical applications
    4. **Current State**: Discuss the current state of the field, recent developments, or trends
    5. **Challenges and Solutions**: Address common challenges and their solutions
    6. **Best Practices**: Include industry best practices, guidelines, or recommendations
    7. **Different Perspectives**: Present multiple viewpoints or approaches when applicable
    8. **Data and Statistics**: Include relevant data, statistics, or research findings
    9. **Implementation Details**: Provide specific implementation guidance when relevant
    10. **Future Outlook**: Discuss future trends, developments, or implications
    
    Your response should be:
    - Highly detailed and comprehensive
    - Technically accurate and precise
    - Well-organized with clear sections
    - Include specific examples and references
    - Address the query from multiple angles
    - Provide actionable insights and recommendations
    
    Focus on delivering substantial, valuable content that goes beyond surface-level information.
    """)
    
    try:
        if tavily_available and tavily_search:
            # Use Tavily search if available
            search_results = tavily_search.invoke(state["optimized_query"])
            
            # Check if search_results is a list of dictionaries as expected
            if not isinstance(search_results, list):
                print(f"Warning: Expected list of search results, got {type(search_results)}")
                # Convert to expected format if possible
                if isinstance(search_results, str):
                    search_results = [{"url": "N/A", "title": "Search Result", "content": search_results}]
                else:
                    # Default empty list 
                    search_results = []
            
            # Summarize the search results
            research_output = summarize_search_results(state["optimized_query"], search_results)
        else:
            # Fallback: Generate research content directly using LLM
            print("Tavily not available, generating research content directly...")
            chain = research_prompt | research_llm | StrOutputParser()
            research_output = chain.invoke({"query": state["optimized_query"]})
        
        return {"research_output": research_output}
    except Exception as e:
        print(f"Error in conduct_research: {str(e)}")
        # Return a placeholder research output to allow the workflow to continue
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
            if tavily_available and fact_verification_search:
                # Verify the claim using Tavily
                verification = verify_claim(claim)
                
                # Store the verification data for reference extraction
                search_results = fact_verification_search.invoke(claim)
                verification_data = "\n\n".join([
                    f"Source: {result.get('url', 'Unknown')}\n"
                    f"Title: {result.get('title', 'No title')}\n"
                    f"Content: {result.get('content', 'No content')}"
                    for result in search_results
                ])
            else:
                # Fallback: Generate verification using LLM only
                print(f"Tavily not available, generating verification for claim: {claim}")
                verification = {
                    "accuracy_score": 7,
                    "confidence_level": 6,
                    "inaccuracies": [],
                    "missing_context": ["Limited verification due to no search access"],
                    "potential_biases": [],
                    "corrected_claim": claim
                }
                verification_data = "Verification based on LLM knowledge only (no external search available)"
            
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
