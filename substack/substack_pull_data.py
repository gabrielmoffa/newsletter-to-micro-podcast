from substack_api import Newsletter


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
            raise Exception(f"No posts found for {newsletter_url}. This could be due to network restrictions or API limitations in GitHub Actions environment.")
        
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