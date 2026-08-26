from markdown_link_resolver.resolver import resolve_markdown_links

# 1. Unser Test-Markdown mit einem echten Bild aus dem Netz
dirty_markdown = "Hier ist ein Testbild: ![Placeholder](https://via.placeholder.com/150)"

# 2. Wir definieren Fake-Header (die via.placeholder.com ignorieren wird, aber sie werden gesendet)
my_headers = {
    "Authorization": "Bearer SUPER_SECRET_TOKEN_123",
    "X-My-Custom-Header": "HelloReddit"
}

print("Starte Download und Konvertierung...\n")

# 3. Funktion aufrufen
clean_markdown = resolve_markdown_links(
    dirty_markdown, 
    base_url="https://example.com", 
    inline_images=True, 
    headers=my_headers
)

print("=== ERGEBNIS ===")
# Wir schneiden den Output ab, damit das Terminal nicht mit Base64-Zeichen geflutet wird
print(clean_markdown[:150] + " ... [Rest des Base64 Strings]")
