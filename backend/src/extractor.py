from pdf2image import convert_from_path
import util
import pytesseract

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailsParser

POPPLER_PATH = r'C:\Users\Mirage\OneDrive\Desktop\Projects\Python Projects\Project Medical Data Extraction\backend\notebooks\poppler-24.02.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image

def extract(file_path, file_format):
    # extracting text from pdf file
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ''

    if len(pages)>0:
        page=pages[0]
        processed_image = util.preprocess_image(page)
        text=pytesseract.image_to_string(processed_image, lang='eng')
        document_text = '\n' + text

    # extract fields from text
    if file_format == 'prescription':
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f'Invalid document format: {file_format}')

    return extracted_data
if __name__=='__main__':
    data = extract('../resources/prescription/pre_1.pdf', 'prescription')
    print(data)