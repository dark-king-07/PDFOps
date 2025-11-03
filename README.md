# 📄 Universal PDF and Image Toolkit

This Python command-line utility provides three core functions for file manipulation: **extracting and merging specific pages from a PDF**, **converting all PDF pages to JPG images**, and **merging a folder of images into a single PDF document**.

It was built using the `PyPDF2`, `pdf2image`, and `Pillow` libraries.

---

## ✨ Features

This script operates in three distinct modes, determined by the arguments you provide:

1.  **Batch PDF Page Extraction:** Extracts specific pages or ranges from an input PDF and saves them as a single merged PDF file.
    * *Input:* `my_document.pdf`, `"1-3, 5, 8"`
2.  **PDF to JPG Conversion:** Renders every page of a PDF into high-quality JPEG images.
    * *Input:* `my_document.pdf`, `to_jpg`
3.  **Images to PDF Creation:** Takes a folder containing JPG/PNG files and merges them into a single, multi-page PDF document.
    * *Input:* `/path/to/image/folder`, `from_images`

---

## ⚙️ Installation and Setup

### 1. Python Dependencies

Install the required Python libraries using `pip`:

```bash
pip install PyPDF2 pdf2image Pillow
```
---
## 2. Poppler (Required for PDF to JPG Conversion)

The **`pdf2image`** library requires the external **Poppler** utility to render PDFs into images.

| OS | Installation Instructions |
| :--- | :--- |
| **Windows** | 1. Download a pre-compiled binary (e.g., from the [Poppler for Windows GitHub releases page](https://github.com/oschwartz10612/poppler-windows/releases/)). <br> 2. Extract the contents (e.g., to `C:\poppler-25.07.0`). <br> 3. **Crucially, update the `POPPLER_PATH` variable** near the top of the `pdf_converter.py` script to point to the `bin` folder within your Poppler directory. <br> *Example:* `POPPLER_PATH = r"C:\poppler-25.07.0\Library\bin"` |
| **Linux (Debian/Ubuntu)** | Run: `sudo apt-get install poppler-utils` |
| **macOS (Homebrew)** | Run: `brew install poppler` |

---

## 🚀 Usage

Execute the script from your command line using the following syntax patterns:

### Mode 1 : Batch PDF Page Extraction

Merges specified pages into a single PDF.

```bash
python pdf_converter.py <input_pdf_path> "<page_numbers_or_ranges>"

# Example: Extract pages 1, 5, and the range 10 through 12.
python pdf_converter.py report.pdf "1, 5, 10-12"
```

### Mode 2 : PDF to JPG Conversion

Converts every page of the PDF to a separate JPG file.

```bash
python pdf_converter.py <input_pdf_path> to_jpg

# Example: Convert all pages of handbook.pdf to JPG.
python pdf_converter.py handbook.pdf to_jpg
```

### Mode 3 : Image Folder to PDF

Merges all supported images in a folder into one PDF file.

```bash
python pdf_converter.py <image_folder_path> from_images

# Example: Convert all images in the Scans folder to a PDF.
python pdf_converter.py ./Scans from_images
```

