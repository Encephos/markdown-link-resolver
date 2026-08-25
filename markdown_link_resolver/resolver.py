import re
from urllib.parse import urljoin, urlparse

def resolve_markdown_links(markdown_text: str, base_url: str) -> str:
    """
    Sucht alle relativen Markdown-Links und Bilder und wandelt sie in absolute URLs um.
    
    Args:
        markdown_text (str): Der rohe Markdown-String.
        base_url (str): Die Basis-URL, gegen die relative Pfade aufgelöst werden sollen.
        
    Returns:
        str: Der Markdown-Text mit absoluten URLs.
    """
    pattern = re.compile(r'(!?\[.*?\])\(\s*([^\s)]+)(?:\s+([^)]+))?\s*\)')

    def _replace_link(match):
        text_part = match.group(1)
        url = match.group(2)
        title = match.group(3)

        # Prüfen, ob die URL bereits absolut ist oder ignoriert werden soll
        is_absolute = bool(urlparse(url).netloc)
        is_special = url.startswith(('mailto:', 'tel:', '#'))

        if is_absolute or is_special:
            new_url = url
        else:
            # urljoin fügt Basis und relativen Pfad sicher zusammen
            new_url = urljoin(base_url, url)

        # Link wieder zusammensetzen (mit oder ohne Titel)
        if title:
            return f'{text_part}({new_url} {title})'
        else:
            return f'{text_part}({new_url})'

    return pattern.sub(_replace_link, markdown_text)