# Markdown Link Resolver

A zero-dependency Python micro-tool to resolve relative links and image paths in Markdown files to absolute URLs. Perfect for web scraping, RAG pipelines, and LLM data preparation.

## Installation

```bash
pip install markdown-link-resolver
```
*(For local development: `pip install -e .`)*

## Basic Usage
```python
from markdown_link_resolver import resolve_markdown_links

base_url = "[https://example.com/blog/](https://example.com/blog/)"
dirty_markdown = "Check out our [about us](../about) page or our ![logo](images/logo.png)."

clean_markdown = resolve_markdown_links(dirty_markdown, base_url)
print(clean_markdown)
# Output: Check out our [about us](https://example.com/about) page or our ![logo](https://example.com/blog/images/logo.png).
```

## Advanced: Base64 Images & Authentication (v0.2.0)
If you are passing scraped data to Multimodal LLMs (like GPT-4o or Claude 3.5), you can automatically inline images as base64 strings.

If the images are behind a login wall, you can pass custom HTTP headers (like a Bearer token or session cookie) to authenticate the download.

```python
auth_headers = {
    "Authorization": "Bearer YOUR_API_TOKEN"
}

md_with_images = "Look at this chart: ![Chart](/assets/private-chart.png)"

prepared_md = resolve_markdown_links(
    md_with_images, 
    base_url="[https://secure.example.com/](https://secure.example.com/)", 
    inline_images=True, 
    headers=auth_headers
)

# Output: Look at this chart: ![Chart](data:image/png;base64,iVBORw0KGgo...)
```

**Graceful Fallbacks:** If an image download times out (5s) or returns a 404, the script gracefully falls back to the absolute URL without crashing your pipeline.
