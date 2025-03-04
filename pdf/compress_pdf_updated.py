import fitz  # PyMuPDF
from PIL import Image
import os
import io
from PyPDF2 import PdfWriter, PdfReader

def compress_pdf(input_pdf_path, output_pdf_path, target_size_kb, initial_quality=90, quality_step=5):
    # 提取PDF中的所有页面并转换为图片
    images = []
    pdf_document = fitz.open(input_pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(dpi=150)  # 设置较低的dpi来减少图片大小
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # 确保图片格式正确
        images.append(img)
    pdf_document.close()

    # 迭代调整图片质量并检查文件大小
    quality = initial_quality
    compressed_pdf_path = "temp_compressed.pdf"

    while True:
        # 压缩所有图片
        compressed_images = []
        for image in images:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=quality)  # 使用JPEG格式，有损压缩
            compressed_images.append(img_byte_arr.getvalue())

        # 生成新的PDF
        pdf_writer = PdfWriter()
        for img_bytes in compressed_images:
            img_pdf = fitz.open()
            img_page = img_pdf.new_page(width=612, height=792)  # 设置合理的页面大小
            img_page.insert_image(img_page.rect, stream=img_bytes)
            pdf_bytes = img_pdf.convert_to_pdf()
            pdf_writer.add_page(PdfReader(io.BytesIO(pdf_bytes)).pages[0])

        # 保存压缩后的PDF
        with open(compressed_pdf_path, "wb") as f:
            pdf_writer.write(f)

        # 检查大小
        if os.path.getsize(compressed_pdf_path) <= target_size_kb * 1024 or quality <= quality_step:
            break

        # 降低质量继续迭代
        quality -= quality_step

    # 保存最终的压缩PDF
    os.rename(compressed_pdf_path, output_pdf_path)
    print(f"Compressed PDF saved as {output_pdf_path} with final quality {quality}")

# 示例使用
input_pdf_path = r'/Users/lanting/Downloads/Sci Bull 2024.pdf'
output_pdf_path = r'/Users/lanting/Downloads/Sci Bull 2024-1.pdf'
target_size_kb = 5000

compress_pdf(input_pdf_path, output_pdf_path, target_size_kb=target_size_kb, initial_quality=90)  # 设定初始图片质量
