from substack_api import Newsletter
import requests
import json
from bs4 import BeautifulSoup
import re


def get_latest_newsletter_via_api(newsletter_url: str) -> tuple[str, str]:
    """Fallback method using direct HTTP requests"""
    try:
        print("Trying fallback method with direct HTTP requests...")
        
        # Get the subdomain from URL
        subdomain = newsletter_url.replace('https://', '').replace('.substack.com', '')
        api_url = f"https://{subdomain}.substack.com/api/v1/posts"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Referer': newsletter_url
        }
        
        print(f"Fetching from API: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        posts = data.get('posts', [])
        
        if not posts:
            print("No posts found in API response")
            return None, None
            
        latest_post = posts[0]
        post_url = f"https://{subdomain}.substack.com/p/{latest_post['slug']}"
        
        # Get the full post content
        print(f"Fetching full post content from: {post_url}")
        post_response = requests.get(post_url, headers=headers, timeout=30)
        post_response.raise_for_status()
        
        return post_response.text, post_url
        
    except Exception as e:
        print(f"Fallback method failed: {str(e)}")
        return None, None


def get_latest_newsletter_html(newsletter_url: str) -> tuple[str, str]:
    """
    Get HTML content and URL of the latest newsletter post
    
    Args:
        newsletter_url: URL of the Substack newsletter (e.g., "https://example.substack.com")
    
    Returns:
        Tuple of (HTML content, specific post URL)
    """
    try:
        print(f"Attempting to fetch from: {newsletter_url}")
        newsletter = Newsletter(newsletter_url)
        print("Newsletter object created successfully")
        
        posts = newsletter.get_posts(limit=1)
        print(f"Retrieved {len(posts) if posts else 0} posts")
        
        if not posts:
            # Try with different limit
            print("No posts with limit=1, trying limit=5...")
            posts = newsletter.get_posts(limit=5)
            print(f"Retrieved {len(posts) if posts else 0} posts with limit=5")
        
        if not posts:
            print("substack-api failed, trying fallback method...")
            html_content, post_url = get_latest_newsletter_via_api(newsletter_url)
            
            if html_content and post_url:
                print(f"Successfully fetched via fallback: {post_url}")
                print(f"Content length: {len(html_content)} characters")
                return html_content, post_url
            else:
                raise Exception(f"Both primary and fallback methods failed to get posts from {newsletter_url}")
        
        latest_post = posts[0]
        post_content = latest_post.get_content()
        post_url = latest_post.url
        
        print(f"Successfully fetched post: {post_url}")
        print(f"Content length: {len(post_content)} characters")
        
        return post_content, post_url
        
    except Exception as e:
        print(f"Error in get_latest_newsletter_html: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        raise


if __name__ == "__main__":
    newsletter_url = "https://giadafromgamma.substack.com"
    html_content, post_url = get_latest_newsletter_html(newsletter_url)
    
    # Save to file (overwrite if exists)
    with open('latest_newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Latest post URL: {post_url}")
    print(f"Saved latest newsletter HTML to latest_newsletter.html ({len(html_content)} characters)")