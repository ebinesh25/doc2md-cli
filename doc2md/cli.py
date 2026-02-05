#!/usr/bin/env python3
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def convert_files(files, output_dir: Path, headless: bool):
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = context.new_page()
        page.goto("https://word2md.com/")

        for file_path in files:
            print(f"⬇ Converting: {file_path.name}")

            with page.expect_file_chooser() as fc_info:
                page.click('input[type="file"]')
            file_chooser = fc_info.value
            file_chooser.set_files(str(file_path))

            page.wait_for_selector("#copy-button", state="visible")
            page.click("#copy-button")

            md_content = page.evaluate("navigator.clipboard.readText()")

            out_file = output_dir / (file_path.stem + ".md")
            out_file.write_text(md_content, encoding="utf-8")

            print(f"✔ Saved: {out_file}")

        browser.close()


def main():
    parser = argparse.ArgumentParser(
        prog="doc2md",
        description="Convert DOCX files to Markdown using word2md.com"
    )

    parser.add_argument(
        "input",
        help="DOCX file or directory containing DOCX files"
    )

    parser.add_argument(
        "--out",
        default="./md",
        help="Output directory (default: ./md)"
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )

    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_dir = Path(args.out).expanduser()

    if not input_path.exists():
        raise SystemExit(f"❌ Path not found: {input_path}")

    # 🔥 NEW LOGIC
    if input_path.is_file():
        if input_path.suffix.lower() != ".docx":
            raise SystemExit("❌ Input file must be a .docx file")
        files = [input_path]

    else:
        files = list(input_path.glob("*.docx"))
        if not files:
            raise SystemExit("❌ No .docx files found")

    convert_files(files, output_dir, args.headless)


if __name__ == "__main__":
    main()
