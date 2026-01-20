from newspaper import Article as NewsArticle


def extract_article(url: str) -> dict:
    article = NewsArticle(url)
    article.download()
    article.parse()

    if not article.text:
        raise ValueError("Failed to extract article body")

    return {
        "title": article.title.strip(),
        "text": article.text.strip()
    }
