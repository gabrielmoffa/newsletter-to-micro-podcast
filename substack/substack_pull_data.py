import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_latest_newsletter_html(newsletter_url: str) -> tuple[str, str]:
    """
    Get HTML content and URL of the latest newsletter post using RSS proxy services
    
    Args:
        newsletter_url: URL of the Substack newsletter (e.g., "https://example.substack.com")
    
    Returns:
        Tuple of (HTML content, specific post URL)
    """
    print(f"Fetching latest newsletter from: {newsletter_url}")
    
    # Get the subdomain from URL
    subdomain = newsletter_url.replace('https://', '').replace('.substack.com', '')
    rss_url = f"https://{subdomain}.substack.com/feed"
    
    # Use RSS proxy services that work reliably in GitHub Actions
    # Add cache-busting parameters to force fresh RSS data
    cache_buster = int(time.time())
    rss_url_with_cache_buster = f"{rss_url}?t={cache_buster}&refresh=1"
    encoded_url = quote(rss_url_with_cache_buster, safe='')
    proxy_services = [
        f"https://api.rss2json.com/v1/api.json?rss_url={encoded_url}",
        f"https://cors-anywhere.herokuapp.com/{rss_url_with_cache_buster}",
        f"https://rss-proxy.herokuapp.com/v1?url={encoded_url}"
    ]
    
    for proxy_url in proxy_services:
        try:
            print(f"Trying RSS proxy service...")
            headers = {'User-Agent': 'Newsletter-to-Podcast Bot'}
            response = requests.get(proxy_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            if 'rss2json' in proxy_url:
                # Handle rss2json format
                data = response.json()
                if data.get('status') == 'ok' and data.get('items'):
                    latest_item = data['items'][0]
                    post_url = latest_item['link']
                    
                    # Get content from RSS description or fetch full post
                    content = latest_item.get('content', latest_item.get('description', ''))
                    if len(content) < 1000:  # If content is too short, fetch full post
                        print("RSS content too short, fetching full post...")
                        post_response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Newsletter Bot)'}, timeout=30)
                        post_response.raise_for_status()
                        content = post_response.text
                    
                    print(f"✅ Successfully fetched newsletter!")
                    print(f"📄 Post URL: {post_url}")
                    print(f"📝 Content length: {len(content)} characters")
                    return content, post_url
            else:
                # Handle direct proxy response
                soup = BeautifulSoup(response.text, 'xml')
                items = soup.find_all('item')
                
                if items:
                    latest_item = items[0]
                    post_url = latest_item.find('link').text.strip()
                    
                    # Get full post content
                    print("Fetching full post content...")
                    post_response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Newsletter Bot)'}, timeout=30)
                    post_response.raise_for_status()
                    
                    print(f"✅ Successfully fetched newsletter!")
                    print(f"📄 Post URL: {post_url}")
                    print(f"📝 Content length: {len(post_response.text)} characters")
                    return post_response.text, post_url
                    
        except Exception as e:
            print(f"Proxy service failed: {str(e)}")
            continue
    
    raise Exception(f"All methods failed to fetch newsletter from {newsletter_url}")


if __name__ == "__main__":
    newsletter_url = "https://giadafromgamma.substack.com"
    html_content, post_url = get_latest_newsletter_html(newsletter_url)
    
    # Save to file (overwrite if exists)
    with open('latest_newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Latest post URL: {post_url}")
    print(f"Saved latest newsletter HTML to latest_newsletter.html ({len(html_content)} characters)")