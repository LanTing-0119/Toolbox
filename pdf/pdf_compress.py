import fitz
import os


def pdf2img(pdf_path, zoom, rotate_angle=0):
    '''
        zoom_x x方向的缩放系数
        zoom_y y方向的缩放系数
        rotation_angle 旋转角度

    '''

    if os.path.exists('.pdf'):       # 临时文件，需为空
        os.removedirs('.pdf')

    os.mkdir('.pdf')
    # open pdf file

    for page_num in list(range(pages_num)):
        page = pdf[page_num] # 处理第一页
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom, zoom).prerotate(rotate_angle)

        pix = page.get_pixmap(matrix=trans, alpha=False)

        save_pic_name = '.pdf/%s.jpg' % str(page_num+1)
        pix.save(save_pic_name)
        print(save_pic_name)
    pdf.close()

def pic2pdf(obj):
    doc = fitz.open()
    for page_num in list(range(pages_num)):
        img = '.pdf/%s.jpg' % str(page_num+1)
        imgdoc = fitz.open(img)                 # 打开图片
        pdfbytes = imgdoc.convert_to_pdf()        # 使用图片创建单页的 PDF
        os.remove(img)  
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)                   # 将当前页插入文档


    if os.path.exists(obj):         # 若文件存在先删除
        os.remove(obj)
    doc.save(obj)                   # 保存pdf文件
    doc.close()

os.chdir(r'/Users/lanting/Documents/整合肿瘤学 临床卷(全三卷)')
pdf_path = '整合肿瘤学——临床卷（腹部盆腔）.pdf'           # 需要压缩的PDF文件
pdf_new_path = 'new_' + pdf_path
zoom = 100
pdf = fitz.open(pdf_path)
pages_num = pdf.page_count


pdf2img(pdf_path, zoom, rotate_angle=0)
# pic2pdf(pdf_new_path)
# os.removedirs('.pdf')


# pdf = fitz.open(pdf_path)
# print(list(range(len(pdf)+1)))


# def covert2pic(zoom):
#     if os.path.exists('.pdf'):       # 临时文件，需为空
#          os.removedirs('.pdf')
#     os.mkdir('.pdf')
#     for pg in range(totaling):
#         page = doc[pg]
#         zoom = int(zoom)            #值越大，分辨率越高，文件越清晰
#         rotate = int(0)
#         print(page)
#         trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).prerotate(rotate)
#         pm = page.get_pixmap(matrix=trans, alpha=False)
      
#         lurl='.pdf/%s.jpg' % str(pg+1)
#         pm._writeIMG(lurl)
#     doc.close()

# def pic2pdf(obj):
#     doc = fitz.open()
#     for pg in range(totaling):
        # img = '.pdf/%s.jpg' % str(pg+1)
#         imgdoc = fitz.open(img)                 # 打开图片
#         pdfbytes = imgdoc.convertToPDF()        # 使用图片创建单页的 PDF
#         os.remove(img)  
#         imgpdf = fitz.open("pdf", pdfbytes)
#         doc.insertPDF(imgpdf)                   # 将当前页插入文档
#     if os.path.exists(obj):         # 若文件存在先删除
#         os.remove(obj)
#     doc.save(obj)                   # 保存pdf文件
#     doc.close()


# def pdfz(sor, obj, zoom):    
#     covert2pic(zoom)
#     pic2pdf(obj)
    
# if __name__  == "__main__":

#     os.chdir(r'/Users/lanting/Downloads')
#     sor = "Sci Bull 2024 Proof.pdf"              # 需要压缩的PDF文件
#     obj = "new" + sor
#     doc = fitz.open(sor) 
#     totaling = doc.page_count
    
#     zoom = 200                     # 清晰度调节，缩放比率
#     pdfz(sor, obj, zoom)
#     os.removedirs('.pdf')
