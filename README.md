# Markdown Link Resolver

A zero-dependency Python micro-tool to resolve relative links and image paths in Markdown files to absolute URLs. Perfect for web scraping, RAG pipelines, and LLM data preparation.

## Installation

```bash
pip install markdown-link-resolver
```
_(For local development: pip install -e .)_

## Usage
```bash
from markdown_link_resolver import resolve_markdown_links

base_url = "[https://example.com/blog/](https://example.com/blog/)"
dirty_markdown = "Check out our [about us](../about) page or our ![logo](images/logo.png)."

clean_markdown = resolve_markdown_links(dirty_markdown, base_url)
print(clean_markdown)
# Output: Check out our [about us](https://example.com/about) page or our ![logo](https://example.com/blog/images/logo.png).
```
