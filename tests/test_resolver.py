import unittest
from markdown_link_resolver import resolve_markdown_links

class TestMarkdownLinkResolver(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/folder/"

    def test_relative_link(self):
        md = "Link: [Test](page.html)"
        expected = "Link: [Test](https://example.com/folder/page.html)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_relative_path_up(self):
        md = "Link: [Test](../page.html)"
        expected = "Link: [Test](https://example.com/page.html)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_absolute_link_ignored(self):
        md = "Link: [Google](https://google.com)"
        expected = "Link: [Google](https://google.com)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_anchor_and_mailto_ignored(self):
        md = "[Anchor](#section) and [Mail](mailto:test@test.com)"
        expected = "[Anchor](#section) and [Mail](mailto:test@test.com)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_images(self):
        md = "Image: ![Alt Text](img/pic.png)"
        expected = "Image: ![Alt Text](https://example.com/folder/img/pic.png)"
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

    def test_link_with_title(self):
        md = '[Text](link.html "My Title")'
        expected = '[Text](https://example.com/folder/link.html "My Title")'
        self.assertEqual(resolve_markdown_links(md, self.base_url), expected)

if __name__ == '__main__':
    unittest.main()