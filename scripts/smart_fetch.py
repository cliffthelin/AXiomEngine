#!/usr/bin/env python3
import sys
import argparse
import asyncio
import httpx
import trafilatura
import html2text

async def fetch_url_content(url: str) -> str:
    """
    Fetches a URL and extracts the main content as Markdown.
    Provides a clean, token-efficient representation for LLMs.
    """
    try:
        # Use a realistic User-Agent to avoid basic blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        }
        
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
            
            # Primary extraction using trafilatura (extracts main article/docs, strips noise)
            extracted = trafilatura.extract(
                html, 
                include_links=True, 
                include_formatting=True,
                include_images=False
            )
            
            if extracted and len(extracted) > 100:
                return f"# Content from: {url}\n\n{extracted}"
            
            # Fallback to html2text if trafilatura yields too little (e.g. index pages)
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = True
            h.body_width = 0
            
            markdown_content = h.handle(html)
            return f"# Raw Content from: {url}\n\n{markdown_content}"
            
    except Exception as e:
        return f"ERROR: Failed to fetch {url}. Reason: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine Smart Fetch (pi-smart-fetch equivalent)")
    parser.add_argument("url", help="The URL to fetch and extract content from")
    args = parser.parse_args()
    
    result = asyncio.run(fetch_url_content(args.url))
    print(result)

if __name__ == "__main__":
    main()
