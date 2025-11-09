# scraper.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

def scrape_wikipedia(url: str) -> Dict[str, Optional[str]]:
    """
    Scrape a Wikipedia article and return cleaned content.
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Dictionary containing:
        - title: Article title
        - content: Cleaned article text
        - error: Error message if scraping failed
    """
    try:
        # Validate URL
        if not is_valid_wikipedia_url(url):
            return {
                "title": None,
                "content": None,
                "error": "Invalid Wikipedia URL. Please provide a valid Wikipedia article URL."
            }
        
        # Send GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = extract_title(soup)
        
        # Extract and clean content
        content = extract_content(soup)
        
        if not content:
            return {
                "title": title,
                "content": None,
                "error": "Could not extract content from the article."
            }
        
        return {
            "title": title,
            "content": content,
            "error": None
        }
        
    except requests.exceptions.Timeout:
        return {
            "title": None,
            "content": None,
            "error": "Request timeout. The Wikipedia server took too long to respond."
        }
    except requests.exceptions.RequestException as e:
        return {
            "title": None,
            "content": None,
            "error": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "title": None,
            "content": None,
            "error": f"Unexpected error: {str(e)}"
        }


def is_valid_wikipedia_url(url: str) -> bool:
    """
    Check if the URL is a valid Wikipedia article URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Wikipedia URL, False otherwise
    """
    wikipedia_pattern = r'https?://(en\.)?wikipedia\.org/wiki/.+'
    return bool(re.match(wikipedia_pattern, url))


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the article title from Wikipedia page.
    
    Args:
        soup: BeautifulSoup object of the page
        
    Returns:
        Article title as string
    """
    # Try to get title from h1 tag with class 'firstHeading'
    title_tag = soup.find('h1', class_='firstHeading')
    if title_tag:
        return title_tag.get_text().strip()
    
    # Fallback: get from page title
    title_tag = soup.find('title')
    if title_tag:
        # Remove " - Wikipedia" suffix
        title = title_tag.get_text().strip()
        title = title.replace(' - Wikipedia', '')
        return title
    
    return "Unknown Title"


def extract_content(soup: BeautifulSoup) -> str:
    """
    Extract and clean the main article content.
    
    Args:
        soup: BeautifulSoup object of the page
        
    Returns:
        Cleaned article text
    """
    # Find the main content div
    content_div = soup.find('div', id='mw-content-text')
    if not content_div:
        return ""
    
    # Get the parser output div (actual article content)
    parser_output = content_div.find('div', class_='mw-parser-output')
    if not parser_output:
        return ""
    
    # Remove unwanted elements
    remove_unwanted_elements(parser_output)
    
    # Extract text from paragraphs and headers
    content_parts = []
    
    for element in parser_output.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol']):
        # Skip empty elements
        text = element.get_text().strip()
        if not text:
            continue
        
        # Add section headers with formatting
        if element.name in ['h2', 'h3', 'h4']:
            # Remove edit links like "[edit]"
            text = re.sub(r'\[edit\]', '', text)
            content_parts.append(f"\n\n## {text}\n")
        
        # Add paragraphs and lists
        elif element.name == 'p':
            content_parts.append(text)
        
        elif element.name in ['ul', 'ol']:
            # Format list items
            list_items = element.find_all('li', recursive=False)
            for item in list_items:
                item_text = item.get_text().strip()
                if item_text:
                    content_parts.append(f"- {item_text}")
    
    # Join all parts
    content = '\n\n'.join(content_parts)
    
    # Clean up the text
    content = clean_text(content)
    
    return content


def remove_unwanted_elements(soup: BeautifulSoup) -> None:
    """
    Remove unwanted HTML elements from the soup object.
    
    Args:
        soup: BeautifulSoup object to clean (modified in place)
    """
    # Elements to remove
    unwanted_selectors = [
        'sup',  # Reference links [1], [2], etc.
        'table',  # Tables
        '.reference',  # Reference sections
        '.reflist',  # Reference lists
        '.navbox',  # Navigation boxes
        '.infobox',  # Infoboxes
        '.thumb',  # Image thumbnails
        '.mw-editsection',  # Edit links
        '#toc',  # Table of contents
        '.toc',  # Table of contents (alternative)
        'style',  # Style tags
        'script',  # Script tags
        '.hatnote',  # Hatnotes (disambiguation notices)
        '.sistersitebox',  # Sister project boxes
        '.noprint',  # Non-printable elements
        '.metadata',  # Metadata
        '.ambox',  # Article message boxes
    ]
    
    for selector in unwanted_selectors:
        for element in soup.select(selector):
            element.decompose()


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove citation markers like [1], [2], [citation needed], etc.
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[citation needed\]', '', text)
    text = re.sub(r'\[edit\]', '', text)
    
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Remove multiple newlines (keep maximum 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def get_article_sections(content: str) -> list:
    """
    Extract section names from the content.
    
    Args:
        content: Article content with sections marked as ## Section Name
        
    Returns:
        List of section names
    """
    sections = []
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('## '):
            section_name = line.replace('## ', '').strip()
            if section_name:
                sections.append(section_name)
    
    return sections

def validate_and_scrape(url: str) -> tuple:
    """
    Convenience function that validates and scrapes in one call.
    
    Args:
        url: Wikipedia URL to scrape
        
    Returns:
        Tuple of (success: bool, result: dict)
    """
    result = scrape_wikipedia(url)
    success = result['error'] is None
    return success, result