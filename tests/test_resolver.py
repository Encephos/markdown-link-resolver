import unittest
from unittest.mock import patch, MagicMock
from markdown_link_resolver import resolve_markdown_links

class TestMarkdownLinkResolver(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/folder/"

    # ==========================================
    # 1. Alte Tests (Markdown Native)
    # ==========================================
    def test_relative_link(self):
        md = "Link: [Test](page.html)"
        expected = "Link: [Test](https://example.com/folder/page.html)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_absolute_link_ignored(self):
        md = "Link: [Google](https://google.com)"
        expected = "Link: [Google](https://google.com)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    # ==========================================
    # 2. Neue Tests (HTML Tags)
    # ==========================================
    def test_html_anchor(self):
        md = 'Klick <a href="../kontakt.html">hier</a>'
        expected = 'Klick <a href="https://example.com/kontakt.html">hier</a>'
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_html_image_with_attributes(self):
        # Prüft, ob Attribute wie class und alt vor und nach dem src unberührt bleiben
        md = '<img class="logo" src="img/logo.png" alt="Mein Logo">'
        expected = '<img class="logo" src="https://example.com/folder/img/logo.png" alt="Mein Logo">'
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_html_single_quotes(self):
        md = "<a href='relativ.html'>Test</a>"
        expected = "<a href='https://example.com/folder/relativ.html'>Test</a>"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    # ==========================================
    # 3. Neue Tests (Base64 Inlining mit Mocks)
    # ==========================================
    @patch('urllib.request.urlopen')
    def test_inline_markdown_image(self, mock_urlopen):
        # Bereite den Mock vor: Simuliere den Download von b"fake_image"
        # "fake_image" in Base64 ist "ZmFrZV9pbWFnZQ=="
        mock_response = MagicMock()
        mock_response.read.return_value = b"fake_image"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        md = "![Bild](pic.png)"
        # Da wir 'pic.png' anfragen, rät mimetypes 'image/png'
        expected = "![Bild](data:image/png;base64,ZmFrZV9pbWFnZQ==)"
        
        result = resolve_markdown_links(md, self.base_url, inline_images=True)
        self.assertEqual(result, expected)

    @patch('urllib.request.urlopen')
    def test_inline_html_image(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"fake_image"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        md = '<img src="pic.jpg">'
        # Fallback auf image/jpeg durch mimetypes bei .jpg
        expected = '<img src="data:image/jpeg;base64,ZmFrZV9pbWFnZQ==">'
        
        result = resolve_markdown_links(md, self.base_url, inline_images=True)
        self.assertEqual(result, expected)

    @patch('urllib.request.urlopen')
    def test_inline_image_fails_gracefully(self, mock_urlopen):
        # Simuliere einen Netzwerkfehler (z.B. 404 oder Timeout)
        mock_urlopen.side_effect = Exception("Netzwerkfehler")

        md = "![Bild](pic.png)"
        # Wenn der Download fehlschlägt, soll einfach die absolute URL genutzt werden
        expected = "![Bild](https://example.com/folder/pic.png)"
        
        result = resolve_markdown_links(md, self.base_url, inline_images=True)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()