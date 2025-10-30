from substack_api import Newsletter


def get_latest_newsletter_html(newsletter_url: str) -> tuple[str, str]:
    """
    Get HTML content and URL of the latest newsletter post
    
    Args:
        newsletter_url: URL of the Substack newsletter (e.g., "https://example.substack.com")
    
    Returns:
        Tuple of (HTML content, specific post URL)
    """
    newsletter = Newsletter(newsletter_url)
    posts = newsletter.get_posts(limit=1)
    
    if not posts:
        raise Exception("No posts found")
    
    latest_post = posts[0]
    return latest_post.get_content(), latest_post.url


if __name__ == "__main__":
    newsletter_url = "https://giadafromgamma.substack.com"
    html_content, post_url = get_latest_newsletter_html(newsletter_url)
    
    # Save to file (overwrite if exists)
    with open('latest_newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Latest post URL: {post_url}")
    print(f"Saved latest newsletter HTML to latest_newsletter.html ({len(html_content)} characters)")