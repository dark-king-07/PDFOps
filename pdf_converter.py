import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image # NEW REQUIRED IMPORT
import glob

# Try to import pdf2image for the 'to_jpg' feature
try:
    from pdf2image import convert_from_path
except ImportError:
    # Define a dummy variable if pdf2image isn't installed, so the script can still run
    convert_from_path = None
    
# --- Global Configuration (for 'to_jpg' feature) ---
# NOTE: Set this variable if using Windows and installed Poppler manually!
# Example: POPPLER_PATH = r"C:\path\to\poppler-xx\bin"
POPPLER_PATH = None 


# --- PDF Page Extraction Logic (Unmodified) ---

def parse_page_input(page_input_str, total_pages):
    # ... (Unmodified parsing logic goes here) ...
    pages_to_extract = set()
    parts = page_input_str.split(',')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        try:
            if '-' in part:
                start_str, end_str = part.split('-', 1)
                start_page = int(start_str.strip())
                end_page = int(end_str.strip())
                
                if start_page < 1 or end_page > total_pages or start_page > end_page:
                    raise ValueError(f"Invalid range or page number out of bounds: {part}")
                    
                for page_num in range(start_page, end_page + 1):
                    pages_to_extract.add(page_num - 1)
            else:
                single_page = int(part)
                
                if not 1 <= single_page <= total_pages:
                    raise ValueError(f"Page number out of bounds: {part}")
                    
                pages_to_extract.add(single_page - 1)
                
        except ValueError as e:
            print(f"❌ Error parsing page input '{part}': {e}. Skipping this part.")
            
    return sorted(list(pages_to_extract))


def batch_extract_pdf_pages(input_pdf_path, pages_to_extract_indices, output_dir="extracted_pages"):
    # ... (Unmodified PDF merging logic goes here) ...
    if not pages_to_extract_indices:
        print("🛑 No valid pages specified for extraction. Exiting.")
        return

    try:
        print(f"📄 Reading PDF: {os.path.basename(input_pdf_path)}")
        with open(input_pdf_path, 'rb') as file:
            reader = PdfReader(file)
            os.makedirs(output_dir, exist_ok=True)
            writer = PdfWriter()
            extracted_pages_1_based = []
            
            for page_index in pages_to_extract_indices:
                page = reader.pages[page_index]
                writer.add_page(page)
                extracted_pages_1_based.append(page_index + 1)

            page_list_str = "_".join(str(p) for p in extracted_pages_1_based)
            if len(page_list_str) > 30:
                 page_list_str = f"{len(extracted_pages_1_based)}_pages"
                 
            output_filename = os.path.join(
                output_dir,
                f"pages_{page_list_str}_of_{os.path.basename(input_pdf_path)}"
            )

            with open(output_filename, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"\n✅ Batch PDF extraction complete!")
            print(f"   -> Extracted {len(extracted_pages_1_based)} pages to: {output_filename}")

    except FileNotFoundError:
        print(f"\n❌ Error: The file '{input_pdf_path}' was not found.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

# --- PDF to JPG Conversion Logic (Unmodified) ---

def convert_pdf_to_jpg(input_pdf_path, output_dir="extracted_images"):
    """Converts all pages of a PDF to separate JPG files."""
    
    if convert_from_path is None:
        print("\n❌ Error: The 'pdf2image' library is not installed, or Poppler is missing. Cannot perform JPG conversion.")
        return

    # Use the global POPPLER_PATH here
    global POPPLER_PATH
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
        
        print(f"\n🖼️ Starting PDF to JPG conversion for {os.path.basename(input_pdf_path)}...")

        images = convert_from_path(
            pdf_path=input_pdf_path, 
            dpi=300, 
            thread_count=4, 
            poppler_path=POPPLER_PATH 
        )

        for i, image in enumerate(images):
            output_filename = os.path.join(output_dir, f"{base_name}_page_{i+1}.jpg")
            image.save(output_filename, 'JPEG')
            print(f"   -> Saved page {i+1} as: {os.path.basename(output_filename)}")

        print(f"\n✅ All {len(images)} pages successfully converted to JPG!")

    except FileNotFoundError:
        print(f"\n❌ Error: The PDF file '{input_pdf_path}' was not found.")
    except Exception as e:
        if "unable to open PDF file" in str(e):
             print("\n❌ Conversion Error: Poppler not found. Ensure it is installed and the POPPLER_PATH variable is correctly set.")
        else:
            print(f"\n❌ An unexpected error occurred during JPG conversion: {e}")


# --- NEW: Image Folder to PDF Conversion Logic ---

def convert_images_to_pdf(input_folder_path, output_filename="merged_images.pdf"):
    """
    Converts all JPG and PNG files in a folder into a single multi-page PDF.
    """
    output_dir = "merged_pdfs"
    os.makedirs(output_dir, exist_ok=True)
    full_output_path = os.path.join(output_dir, output_filename)
    
    # 1. Find all image files (case-insensitive)
    image_paths = []
    # Use glob to find JPG and PNG files
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_paths.extend(glob.glob(os.path.join(input_folder_path, ext), recursive=False))
        
    image_paths.sort() # Ensure images are ordered by name (e.g., page1.jpg, page2.jpg)
    
    if not image_paths:
        print(f"\n🛑 Error: No JPG or PNG images found in folder: {input_folder_path}")
        return

    print(f"\n🖼️ Found {len(image_paths)} images. Starting merge to PDF...")
    
    try:
        # 2. Open the first image (which becomes the first page)
        first_image_path = image_paths[0]
        first_image = Image.open(first_image_path).convert('RGB')
        
        # 3. Prepare the list of remaining images
        remaining_images = []
        for path in image_paths[1:]:
            # Convert to RGB to ensure compatibility with PDF format
            remaining_images.append(Image.open(path).convert('RGB'))
            
        # 4. Save the first image, appending the rest of the images
        first_image.save(
            full_output_path, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=remaining_images
        )
        
        print(f"\n✅ Successfully merged {len(image_paths)} images into a PDF!")
        print(f"   -> Output saved to: {full_output_path}")

    except FileNotFoundError:
        print(f"\n❌ Error: The image folder '{input_folder_path}' was not found.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during PDF creation: {e}")


# --- Main execution block for command-line arguments ---
if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Usage (Extract Pages): python script.py <input_pdf_path> \"<page_numbers_or_ranges>\"")
        print("Usage (PDF to JPG):    python script.py <input_pdf_path> to_jpg")
        print("Usage (Images to PDF): python script.py <image_folder_path> from_images")
        print("\nExample 1 (Extract): python script.py my_doc.pdf \"1, 3-5\"")
        print("Example 2 (To JPG):  python script.py my_doc.pdf to_jpg")
        print("Example 3 (From Img): python script.py C:\\Users\\Images from_images")
        sys.exit(1)

    input_path_or_folder = sys.argv[1]
    mode_arg = sys.argv[2]
    
    if mode_arg.lower() == "to_jpg":
        # Mode 2: PDF to JPG
        convert_pdf_to_jpg(input_path_or_folder)
        
    elif mode_arg.lower() == "from_images":
        # Mode 3: Image Folder to PDF
        convert_images_to_pdf(input_path_or_folder)
        
    else:
        # Mode 1: PDF Page Extraction/Merging
        try:
            with open(input_path_or_folder, 'rb') as file:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
        except FileNotFoundError:
            print(f"\n❌ Error: The PDF file '{input_path_or_folder}' was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ An error occurred while reading the PDF: {e}")
            sys.exit(1)

        pages_indices = parse_page_input(mode_arg, total_pages)
        batch_extract_pdf_pages(input_path_or_folder, pages_indices)
