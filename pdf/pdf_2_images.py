import os
from pdf2image import convert_from_path
import time

# time.sleep(600)



# Configuration
pdf_directory = '/Users/lanting/Documents/整合肿瘤学 临床卷(全三卷)'  # Replace with your PDF directory path
output_directory = '/Users/lanting/Documents/outputs'  # Replace with your desired output path

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# List all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]

file_counter = 1  # Initialize file naming counter
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    print(f'Processing {pdf_path}...')
    
    # Convert PDF to images
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f'Error converting {pdf_file}: {e}')
        continue

    # Save each page as a PNG file
    image_counter = 1  # Initialize image naming counter
    for page_number, image in enumerate(images, start=1):
        image_filename = f'{file_counter}_{image_counter}.png'
        image_path = os.path.join(output_directory, image_filename)
        image.save(image_path, 'PNG')
        print(f'Saved {image_path}')
        image_counter += 1

    file_counter += 1

print('Conversion completed!')
