import pytesseract
from wand.image import Image as wi
from PIL import Image
import io


def get_text_from_pdf(pdf_path):
    pdf = wi(filename=pdf_path, resolution=100)
    pdfImg = pdf.convert('jpeg')
    img_blobs = []
    extracted_text = []

    for img in pdfImg.sequence:
        page = wi(image=img)
        img_blobs.append(page.make_blob('jpeg'))

    for img_blob in img_blobs:
        im = Image.open(io.BytesIO(img_blob))
        text = pytesseract.image_to_string(im, lang='eng')
        extracted_text.append(text)

    return extracted_text


def get_text_from_pdf_blob(pdf):
    pdf = wi(filename=pdf, resolution=100)
    pdfImg = pdf.convert('jpeg')
    img_blobs = []
    extracted_text = []

    for img in pdfImg.sequence:
        page = wi(image=img)
        img_blobs.append(page.make_blob('jpeg'))

    for img_blob in img_blobs:
        im = Image.open(io.BytesIO(img_blob))
        text = pytesseract.image_to_string(im, lang='eng')
        extracted_text.append(text)

    # Render extracted_text to html format
    r = '<br />'
    extracted_text = [_.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r) for _ in extracted_text]
    return extracted_text

e_t = get_text_from_pdf_blob(r'/Users/a/PycharmProjects/sentence-sentiment/static/pdf/test_pdf.pdf')
# e_t = get_text_from_image(r'/Users/a/PycharmProjects/sentence-sentiment/static/pdf/test_pdf.pdf')