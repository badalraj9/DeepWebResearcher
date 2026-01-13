# DeepWebResearcher V2

A powerful, cost-effective AI Research Agent backend that leverages a **"Free Stack"** architecture to minimize API costs while delivering deep, verified insights.

Built with **FastAPI**, **LangGraph**, and **Playwright**.

## 🚀 What's New in V2?

The V2 update introduces a **Smart Router** that drastically reduces reliance on paid Search APIs (like Tavily) by prioritizing robust, free alternatives:

*   **Smart Routing**: Automatically detects if a query is a "Simple Fact", "Deep Research", or "Direct URL" and routes it to the most efficient tool.
*   **The "Free Stack"**:
    *   **Search**: Uses **DuckDuckGo** (via `ddgs`) for unlimited, high-quality search results without monthly quotas.
    *   **Deep Scraping**: Uses **Playwright** (Headless Chromium) to visit, render, and scrape full content from top search results, including modern JS-heavy websites that standard scrapers fail on.
*   **Direct URL Scraping**: Simply paste a URL (e.g., `https://example.com/article`) and the agent will scrape, analyze, and summarize it directly.
*   **Robust Fallbacks**: seamlessly falls back to paid tools (Tavily/Exa) only if the free stack encounters edge cases or blocking.

## ✨ Features

*   **🤖 Agentic Research**: Autonomous workflows that search, scrape, read, and synthesize information.
*   **🕵️‍♂️ Deep Web Scraping**: Renders dynamic JavaScript content to "see" what users see.
*   **✅ Fact-Checking**: rigorous verification step that cross-references claims against search snippets.
*   **📝 Multi-Style Reporting**: Generates output in various formats:
    *   Blog Post
    *   Detailed Report
    *   Executive Summary
    *   LaTeX Academic Papers
*   **📚 Library System**: Save and manage your research drafts.

## 🛠️ Setup Guide

### 1. Prerequisites
*   Python 3.10+
*   An [OpenRouter](https://openrouter.ai/) API Key (for the LLM).

### 2. Installation

Clone the repository and navigate to the backend folder:

```bash
cd DeepWebResearcher
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

**Important**: Install the Playwright browsers (required for V2 scraping):

```bash
playwright install chromium
```

### 3. Configuration

Create a `.env` file in the `DeepWebResearcher` directory:

```ini
# Required
OPENROUTER_API_KEY=sk-or-v1-...

# Optional (Fallbacks for V2)
TAVILY_API_KEY=tvly-...
EXA_API_KEY=...
```

*Note: The V2 agent works fully without Tavily, but adding it provides an extra layer of reliability.*

### 4. Running the Server

Start the FastAPI backend:

```bash
python app.py
```

The server will be available at `http://localhost:5000`.

## 🧠 Architecture Overview

1.  **Input**: User provides a query (e.g., "Trends in AI 2025") or a specific URL.
2.  **Smart Router**:
    *   *Is it a URL?* -> **Playwright** visits directly.
    *   *Is it a Search?* -> **DuckDuckGo** fetches organic results.
3.  **Deep Dive**: The agent selects the top 3-5 most relevant results and uses **Playwright** to "read" the full pages (not just snippets).
4.  **Synthesis**: The LLM (`xiaomi/mimo-v2-flash` or similar) analyzes the full content, extracts claims, verifies them, and writes the final report.

## 🤝 Contributing

Contributions are welcome! Please check the `v2` branch for the latest development.
