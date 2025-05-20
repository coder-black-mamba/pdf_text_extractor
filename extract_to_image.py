from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import os
import io

def convert_pdf_to_images(pdf_path, output_dir="pdf_images", dpi=300, format="PNG"):
    """
    Convert PDF pages to images using pdf2image library.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save converted images
        dpi (int): Resolution of output images (higher = better quality)
        format (str): Output image format (PNG, JPEG, TIFF, etc.)
    
    Returns:
        list: List of saved image file paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)
        image_paths = []
        
        # Save each page as an image
        for i, image in enumerate(images):
            filename = f"page_{i + 1}.{format.lower()}"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath, format=format.upper())
            image_paths.append(filepath)
            print(f"Saved page {i + 1}: {filepath}")
        
        return image_paths
        
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []

def convert_pdf_bytes_to_images(pdf_bytes, output_dir="pdf_images", dpi=300, format="PNG"):
    """
    Convert PDF from bytes to images.
    
    Args:
        pdf_bytes (bytes): PDF file as bytes
        output_dir (str): Directory to save converted images
        dpi (int): Resolution of output images
        format (str): Output image format
    
    Returns:
        list: List of saved image file paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Convert PDF bytes to images
        images = convert_from_bytes(pdf_bytes, dpi=dpi)
        image_paths = []
        
        # Save each page as an image
        for i, image in enumerate(images):
            filename = f"page_{i + 1}.{format.lower()}"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath, format=format.upper())
            image_paths.append(filepath)
            print(f"Saved page {i + 1}: {filepath}")
        
        return image_paths
        
    except Exception as e:
        print(f"Error converting PDF bytes to images: {e}")
        return []

def convert_specific_pages(pdf_path, pages, output_dir="pdf_images", dpi=300, format="PNG"):
    """
    Convert specific pages of PDF to images.
    
    Args:
        pdf_path (str): Path to the PDF file
        pages (list): List of page numbers to convert (1-indexed)
        output_dir (str): Directory to save converted images
        dpi (int): Resolution of output images
        format (str): Output image format
    
    Returns:
        list: List of saved image file paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Convert specific pages to images
        # Note: pdf2image uses 1-indexed pages, but first_page and last_page are inclusive
        images = convert_from_path(pdf_path, dpi=dpi, first_page=min(pages), last_page=max(pages))
        image_paths = []
        
        # Filter and save only requested pages
        for i, page_num in enumerate(sorted(pages)):
            if i < len(images):
                image = images[page_num - min(pages)]
                filename = f"page_{page_num}.{format.lower()}"
                filepath = os.path.join(output_dir, filename)
                image.save(filepath, format=format.upper())
                image_paths.append(filepath)
                print(f"Saved page {page_num}: {filepath}")
        
        return image_paths
        
    except Exception as e:
        print(f"Error converting specific pages: {e}")
        return []

def convert_with_custom_settings(pdf_path, output_dir="pdf_images", **kwargs):
    """
    Convert PDF to images with custom settings.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save converted images
        **kwargs: Additional arguments for pdf2image
            - dpi (int): Resolution (default: 200)
            - format (str): Output format (default: 'PNG')
            - thread_count (int): Number of threads to use
            - userpw (str): PDF password if needed
            - use_cropbox (bool): Use crop box instead of media box
            - strict (bool): Enable strict mode
    
    Returns:
        list: List of saved image file paths
    """
    # Default settings
    settings = {
        'dpi': 200,
        'format': 'PNG',
        'thread_count': 1,
        'use_cropbox': False,
        'strict': False
    }
    
    # Update with provided kwargs
    settings.update(kwargs)
    output_format = settings.pop('format')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Convert PDF to images with custom settings
        images = convert_from_path(pdf_path, **settings)
        image_paths = []
        
        # Save each page as an image
        for i, image in enumerate(images):
            filename = f"page_{i + 1}.{output_format.lower()}"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath, format=output_format.upper())
            image_paths.append(filepath)
            print(f"Saved page {i + 1}: {filepath}")
        
        return image_paths
        
    except Exception as e:
        print(f"Error converting with custom settings: {e}")
        return []

def get_pdf_info(pdf_path):
    """
    Get basic information about the PDF.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        dict: Dictionary with PDF information
    """
    try:
        # Convert just to get page count (low DPI for speed)
        images = convert_from_path(pdf_path, dpi=50)
        
        info = {
            'page_count': len(images),
            'file_size_mb': os.path.getsize(pdf_path) / (1024 * 1024),
            'filename': os.path.basename(pdf_path)
        }
        
        # Get dimensions of first page
        if images:
            first_page = images[0]
            info['page_dimensions'] = first_page.size
            info['page_mode'] = first_page.mode
        
        return info
        
    except Exception as e:
        print(f"Error getting PDF info: {e}")
        return {}

# Example usage
if __name__ == "__main__":
    # Example PDF file path
    pdf_file = "files/1.pdf"  # Replace with your PDF file path
    
    try:
        # Basic conversion
        print("Converting PDF to images...")
        image_files = convert_pdf_to_images(pdf_file, dpi=300, format="PNG")
        print(f"Converted {len(image_files)} pages to images")
        
        # Get PDF info
        # print("\nGetting PDF information...")
        # pdf_info = get_pdf_info(pdf_file)
        # print(f"PDF Info: {pdf_info}")
        
        # # Convert specific pages
        # print("\nConverting specific pages (1, 3, 5)...")
        # specific_pages = convert_specific_pages(pdf_file, [1, 3, 5], output_dir="specific_pages")
        # print(f"Converted {len(specific_pages)} specific pages")
        
        # # Convert with custom settings
        # print("\nConverting with custom settings...")
        # custom_images = convert_with_custom_settings(
        #     pdf_file,
        #     output_dir="custom_images",
        #     dpi=150,
        #     format="JPEG",
        #     thread_count=2,
        #     use_cropbox=True
        # )
        # print(f"Converted {len(custom_images)} pages with custom settings")
        
        # Example with password-protected PDF
        # password_images = convert_with_custom_settings(
        #     "protected.pdf",
        #     output_dir="password_images",
        #     userpw="your_password_here"
        # )
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have pdf2image installed: pip install pdf2image")
        print("Also ensure poppler is installed on your system:")