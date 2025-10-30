from substack_api import Newsletter
import requests
import json
from bs4 import BeautifulSoup
import re
from urllib.parse import quote


def get_latest_newsletter_via_rss(newsletter_url: str) -> tuple[str, str]:
    """Fallback method using RSS feed with multiple retry strategies"""
    import time
    import random
    
    # Multiple user agents to rotate through
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'curl/7.68.0',
        'feedparser/6.0.10',
        'Python-urllib/3.11'
    ]
    
    # Get the subdomain from URL
    subdomain = newsletter_url.replace('https://', '').replace('.substack.com', '')
    rss_url = f"https://{subdomain}.substack.com/feed"
    
    # Try multiple approaches
    for attempt in range(3):
        try:
            print(f"RSS attempt {attempt + 1}/3...")
            
            # Rotate user agent
            user_agent = random.choice(user_agents)
            
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/rss+xml, application/xml, text/xml, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none'
            }
            
            print(f"Using User-Agent: {user_agent[:50]}...")
            print(f"Fetching RSS feed from: {rss_url}")
            
            # Add some randomness to avoid bot detection
            if attempt > 0:
                delay = random.uniform(1, 3)
                print(f"Waiting {delay:.1f} seconds...")
                time.sleep(delay)
            
            session = requests.Session()
            response = session.get(rss_url, headers=headers, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            print(f"RSS feed fetched successfully! Content length: {len(response.text)}")
            
            # Parse RSS feed
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('item')
            
            if not items:
                print("No items found in RSS feed")
                continue
                
            latest_item = items[0]
            post_url = latest_item.find('link').text.strip()
            
            print(f"Found latest post URL from RSS: {post_url}")
            
            # Get the full post content with same session
            print(f"Fetching full post content...")
            post_response = session.get(post_url, headers=headers, timeout=30)
            post_response.raise_for_status()
            
            print(f"Successfully fetched post content! Length: {len(post_response.text)}")
            return post_response.text, post_url
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error on attempt {attempt + 1}: {e}")
            if e.response.status_code == 403:
                print("403 Forbidden - trying different approach...")
                continue
            else:
                break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                continue
            else:
                break
    
    print("All RSS attempts failed, trying proxy services...")
    
    # Try RSS proxy services as last resort
    encoded_url = quote(rss_url, safe='')
    proxy_services = [
        f"https://api.rss2json.com/v1/api.json?rss_url={encoded_url}",
        f"https://cors-anywhere.herokuapp.com/{rss_url}",
        f"https://rss-proxy.herokuapp.com/v1?url={encoded_url}"
    ]
    
    for proxy_url in proxy_services:
        try:
            print(f"Trying proxy: {proxy_url[:50]}...")
            headers = {'User-Agent': 'RSS Reader'}
            response = requests.get(proxy_url, headers=headers, timeout=30)
            
            if 'rss2json' in proxy_url:
                # Handle rss2json format
                data = response.json()
                if data.get('status') == 'ok' and data.get('items'):
                    latest_item = data['items'][0]
                    post_url = latest_item['link']
                    
                    # Get content from RSS description or fetch full post
                    content = latest_item.get('content', latest_item.get('description', ''))
                    if len(content) < 1000:  # If content is too short, fetch full post
                        post_response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; RSS Reader)'}, timeout=30)
                        content = post_response.text
                    
                    print(f"Success via rss2json! Post: {post_url}")
                    return content, post_url
            else:
                # Handle direct proxy response
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'xml')
                items = soup.find_all('item')
                
                if items:
                    latest_item = items[0]
                    post_url = latest_item.find('link').text.strip()
                    
                    # Get full post content
                    post_response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; RSS Reader)'}, timeout=30)
                    
                    print(f"Success via proxy! Post: {post_url}")
                    return post_response.text, post_url
                    
        except Exception as e:
            print(f"Proxy failed: {str(e)}")
            continue
    
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
            print("substack-api failed, trying RSS feed method...")
            html_content, post_url = get_latest_newsletter_via_rss(newsletter_url)
            
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