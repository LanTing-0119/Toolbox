# Path to the folder containing the PNG files
folder_path = "/Users/lanting/Downloads/screenshot/目录_output"
# Specify the output PDF path
output_pdf = "/Users/lanting/Downloads/screenshot/output.pdf"


from PIL import Image
import os
from natsort import natsorted

# Get a sorted list of PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
png_files = natsorted(png_files) # Optional: sorts files by name

# Create a list to store the image objects
images = []

# trace the process
num = 1
all_num = len(png_files)

# Open each PNG file and append it to the images list
for png_file in png_files:
    print(f'{num}/{all_num}')
    img_path = os.path.join(folder_path, png_file)
    img = Image.open(img_path)
    images.append(img.convert('RGB'))  # Convert PNG to RGB mode (required for PDF)
    num = num + 1

# Save the images as a PDF (the first image will be the cover page)
images[0].save(output_pdf, save_all=True, append_images=images[1:], resolution=100.0, quality=95, optimize=True)

print(f"PDF created successfully: {output_pdf}")
