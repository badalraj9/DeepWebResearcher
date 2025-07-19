#!/usr/bin/env python3
"""
Test script for LaTeX Detailed Report functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from draftagent import conduct_research_workflow, select_content_style

def test_latex_report():
    """Test the LaTeX detailed report functionality"""
    
    print("🧪 Testing LaTeX Detailed Report Functionality")
    print("=" * 50)
    
    # Test query
    test_query = "Artificial Intelligence in Healthcare"
    
    print(f"📝 Test Query: {test_query}")
    print(f"🎨 Content Style: LaTeX Detailed Report (Style 4)")
    
    try:
        # Test the content style selection
        content_style = select_content_style(4)
        print(f"✅ Content Style Selected: {content_style}")
        
        # Conduct research with LaTeX style
        print("\n🔍 Conducting research with LaTeX detailed report style...")
        result = conduct_research_workflow(test_query, content_style)
        
        if result.get("status") == "completed":
            print("✅ Research completed successfully!")
            
            # Check if the draft content has LaTeX structure
            draft_content = result.get('draft_content', '')
            
            print(f"\n📊 Results Summary:")
            print(f"   - Research Output Length: {len(result.get('research_output', ''))} characters")
            print(f"   - Draft Content Length: {len(draft_content)} characters")
            print(f"   - References Count: {len(result.get('references', []))}")
            
            # Check for LaTeX structure indicators
            latex_indicators = [
                "Title:", "Abstract", "Introduction", "Methodology", 
                "Results and Findings", "Discussion", "Conclusion", "References"
            ]
            
            found_indicators = []
            for indicator in latex_indicators:
                if indicator.lower() in draft_content.lower():
                    found_indicators.append(indicator)
            
            print(f"\n📋 LaTeX Structure Check:")
            print(f"   - Found {len(found_indicators)} LaTeX structure indicators")
            for indicator in found_indicators:
                print(f"     ✅ {indicator}")
            
            if len(found_indicators) >= 5:
                print("\n🎉 LaTeX Detailed Report test PASSED!")
                print("   The report contains proper LaTeX-style structure.")
            else:
                print("\n⚠️  LaTeX Detailed Report test PARTIAL")
                print("   Some LaTeX structure elements may be missing.")
            
            # Show a preview of the content
            print(f"\n📄 Content Preview (first 500 characters):")
            print("-" * 50)
            print(draft_content[:500] + "..." if len(draft_content) > 500 else draft_content)
            print("-" * 50)
            
        else:
            print("❌ Research failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if required API keys are set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("   Please set your OpenRouter API key in the .env file")
        sys.exit(1)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ TAVILY_API_KEY not found in environment variables")
        print("   Please set your Tavily API key in the .env file")
        sys.exit(1)
    
    # Run the test
    test_latex_report() 