import re
import base64
import mimetypes
import urllib.request
from urllib.parse import urljoin, urlparse

def _url_to_base64(url: str, headers: dict = None) -> str:
    """Lädt ein Bild herunter und konvertiert es in einen Base64-Data-String."""
    try:
        # Ein Standard-User-Agent schützt vor Basic-Blockern
        req_headers = {'User-Agent': 'MarkdownLinkResolver/1.2'}
        
        # Benutzerdefinierte Header (z.B. Auth-Tokens) hinzufügen oder überschreiben
        if headers:
            req_headers.update(headers)
            
        req = urllib.request.Request(url, headers=req_headers)
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            
            # MIME-Type anhand der Endung raten, sonst aus dem Response-Header lesen
            mime_type, _ = mimetypes.guess_type(url)
            if not mime_type:
                mime_type = response.headers.get('Content-Type', 'image/jpeg')
            
            b64_str = base64.b64encode(data).decode('utf-8')
            return f"data:{mime_type};base64,{b64_str}"
            
    except Exception:
        # Wenn der Download fehlschlägt (z.B. 404, Auth-Error oder Timeout), 
        # geben wir die URL einfach als Fallback unverändert zurück.
        return url

def resolve_markdown_links(markdown_text: str, base_url: str, inline_images: bool = False, headers: dict = None) -> str:
    """
    Löst relative URLs in Markdown- und HTML-Tags auf.
    Kann optional Bilder herunterladen und als Base64 einbetten.
    Unterstützt benutzerdefinierte HTTP-Headers (z.B. für Authentifizierung).
    """
    
    # 1. Native Markdown-Links und -Bilder
    md_pattern = re.compile(r'(!?\[.*?\])\(\s*([^\s)]+)(?:\s+([^)]+))?\s*\)')
    
    def md_repl(match):
        text_part = match.group(1)
        url = match.group(2)
        title = match.group(3)
        
        is_absolute = bool(urlparse(url).netloc)
        is_special = url.startswith(('mailto:', 'tel:', '#', 'data:'))
        
        # Absolute URL bilden
        new_url = url if (is_absolute or is_special) else urljoin(base_url, url)
        
        # Base64 Logik: Nur für Bilder (![...]) und gültige HTTP(S)-URLs
        if inline_images and text_part.startswith('!') and new_url.startswith('http'):
            new_url = _url_to_base64(new_url, headers=headers)

        if title:
            return f'{text_part}({new_url} {title})'
        return f'{text_part}({new_url})'

    resolved_md = md_pattern.sub(md_repl, markdown_text)

    # 2. HTML <a> und <img> Tags im Markdown
    # Sucht nach <a ... href="url"> oder <img ... src="url">
    html_pattern = re.compile(r'(<(?:a|img)\b[^>]*\b(?:href|src)\s*=\s*)(["\'])(.*?)\2', re.IGNORECASE)
    
    def html_repl(match):
        prefix = match.group(1) # Z.B. '<img class="logo" src='
        quote = match.group(2)  # Z.B. '"'
        url = match.group(3)    # Z.B. '../logo.png'
        
        is_absolute = bool(urlparse(url).netloc)
        is_special = url.startswith(('mailto:', 'tel:', '#', 'data:'))
        
        # Absolute URL bilden
        new_url = url if (is_absolute or is_special) else urljoin(base_url, url)
        
        # Base64 Logik: Nur für <img ...> Tags
        if inline_images and prefix.lower().startswith('<img') and new_url.startswith('http'):
            new_url = _url_to_base64(new_url, headers=headers)
                
        return f"{prefix}{quote}{new_url}{quote}"
        
    return html_pattern.sub(html_repl, resolved_md)
