import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a scanned Bangla PDF using OCR
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        # Process each page
        all_text = []
        for i, image in enumerate(images):
            print(f"Processing page {i+1}...")
            
            # Convert image to grayscale
            image = image.convert('L')
            
            # Apply threshold to improve OCR accuracy
            image = image.point(lambda x: 0 if x < 128 else 255, '1')
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(image, lang='ben')
            all_text.append(f"Page {i+1}:\n{text}\n\n")
            
        return ''.join(all_text)
    except Exception as e:
        print(f"Error: {str(e)}")
        return ""

def main():
    # Get all PDF files in the files directory
    files_dir = 'files'
    if not os.path.exists(files_dir):
        print(f"Directory '{files_dir}' not found!")
        return
        
    # Get all PDF files
    pdf_files = [f for f in os.listdir(files_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the directory!")
        return
        
    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(files_dir, pdf_file)
        print(f"\nProcessing file: {pdf_file}")
        
        # Extract text
        print("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(pdf_path)
        
        # Save to output file
        output_path ="extracted_text/" + os.path.splitext(pdf_file)[0] + '_extracted.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
            
        print(f"Text extracted and saved to: {output_path}")
    
    print("All files processed.")

if __name__ == "__main__":
    main()
