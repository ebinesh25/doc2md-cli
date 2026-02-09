"""
doc-to-md-cli: Convert DOCX files to Markdown using Playwright
"""

from pathlib import Path
from playwright.sync_api import sync_playwright


__version__ = "0.1.1"


def convert_docx_to_md(
    input_path: str | Path,
    output_dir: str | Path = "./md",
    headless: bool = True,
) -> list[Path]:
    """
    Convert DOCX file(s) to Markdown.

    Args:
        input_path: Path to a DOCX file or directory containing DOCX files
        output_dir: Directory where Markdown files will be saved
        headless: Whether to run browser in headless mode

    Returns:
        List of paths to the generated Markdown files

    Raises:
        FileNotFoundError: If input_path doesn't exist
        ValueError: If no DOCX files found

    Example:
        >>> from doc2md import convert_docx_to_md
        >>> convert_docx_to_md("document.docx", "output")
        ['output/document.md']
    """
    input_path = Path(input_path).expanduser()
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Path not found: {input_path}")

    # Determine files to convert
    if input_path.is_file():
        if input_path.suffix.lower() != ".docx":
            raise ValueError("Input file must be a .docx file")
        files = [input_path]
    else:
        files = list(input_path.glob("*.docx"))
        if not files:
            raise ValueError("No .docx files found in directory")

    converted_files = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()
        page.goto("https://word2md.com/")

        for file_path in files:
            page.goto("https://word2md.com/")

            with page.expect_file_chooser() as fc_info:
                page.click('input[type="file"]')
            file_chooser = fc_info.value
            file_chooser.set_files(str(file_path))

            page.wait_for_selector("#copy-button", state="visible")
            page.click("#copy-button")

            md_content = page.evaluate("navigator.clipboard.readText()")

            out_file = output_dir / (file_path.stem + ".md")
            out_file.write_text(md_content, encoding="utf-8")
            converted_files.append(out_file)

        browser.close()

    return converted_files


__all__ = ["convert_docx_to_md", "__version__"]
