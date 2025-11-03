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
