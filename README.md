# doc-to-md-cli

A Python library and CLI tool to convert DOCX files to Markdown using Playwright automation.

## Features

- Convert single DOCX files or entire directories
- Batch processing support
- Headless browser mode for automation
- Clean Markdown output powered by word2md.com
- Use as a CLI tool or import as a Python library

## Installation

```bash
pip install doc-to-md-cli
```

Install Playwright browser (required):

```bash
playwright install chromium
```

## Usage

### CLI

Convert a single file:

```bash
doc-to-md document.docx
```

Convert to a specific output directory:

```bash
doc-to-md document.docx --out ./output
```

Convert all DOCX files in a directory:

```bash
doc-to-md ./my-docs --out ./converted
```

Show browser window (non-headless mode):

```bash
doc-to-md document.docx --no-headless
```

### Python API

```python
from doc2md import convert_docx_to_md

# Convert a single file
files = convert_docx_to_md("document.docx", "output")
print(files)  # ['output/document.md']

# Convert all files in a directory
files = convert_docx_to_md("./my-docs", "output")
# ['output/file1.md', 'output/file2.md', ...]

# Convert with browser visible
files = convert_docx_to_md("document.docx", headless=False)
```

## Requirements

- Python 3.8 or higher
- Playwright (installed automatically)

## License

MIT License - see LICENSE file for details.
