# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


def clean_newsletter_html(html_content: str) -> str:
    """
    Clean up the newsletter HTML content and extract only the text content
    
    Args:
        html_content: Raw HTML content to clean
    
    Returns:
        Cleaned text content
    """
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements but keep structure
    for element in soup(['script', 'style', 'img', 'figure', 'span']):
        element.decompose()
    
    # For links, keep the text content but remove the link
    for link in soup.find_all('a'):
        link.replace_with(link.get_text())
    
    # Add line breaks after block elements to preserve structure
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'blockquote', 'hr']):
        element.insert_after('\n\n')
    
    # Get text content
    text = soup.get_text()
    
    # Clean up the text while preserving paragraph structure
    text = re.sub(r'\n{3,}', '\n\n', text)    # Replace 3+ newlines with double newline
    text = re.sub(r'[ \t]+', ' ', text)       # Replace multiple spaces/tabs with single space
    text = re.sub(r' *\n *', '\n', text)      # Clean up spaces around newlines
    text = text.strip()                        # Remove leading/trailing whitespace
    
    # Remove button text and other UI elements
    text = re.sub(r'more info.*', '', text)
    text = re.sub(r'Subscribe', '', text)
    text = re.sub(r'Type your email.*', '', text)
    
    # Clean up any remaining artifacts
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 2:  # Keep lines with actual content
            cleaned_lines.append(line)
    
    # Join back with proper spacing
    cleaned_text = '\n\n'.join(cleaned_lines)
    
    return cleaned_text


if __name__ == "__main__":
    # Example usage with file input for testing
    try:
        with open('latest_newsletter.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        cleaned_content = clean_newsletter_html(html_content)
        print(f"Original HTML length: {len(html_content)} characters")
        print(f"Cleaned text length: {len(cleaned_content)} characters")
        print("\nFirst 500 characters:")
        print(cleaned_content[:500])
        
    except FileNotFoundError:
        print("latest_newsletter.html not found. This function now works with HTML content directly.")