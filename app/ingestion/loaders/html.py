from bs4 import BeautifulSoup
import logfire


def parse_html(file_path: str) -> str:
    """
    Parses HTML content using BeautifulSoup.
    Cleans scripts, styles, and extracts readable text for RAG.
    """

    with logfire.span("📄 HTML Parsing", filename=file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, "html.parser")

            # Remove unwanted tags
            for tag in soup(["script", "style", "meta", "noscript"]):
                tag.decompose()

            # Extract text
            text = soup.get_text(separator="\n")

            # Clean whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_clean = "\n".join(chunk for chunk in chunks if chunk)

            return text_clean

        except Exception as e:
            logfire.error(f"❌ HTML Parse Failed: {e}")
            raise