import fitz
import re

def extract_text_from_pdf(pdf_path):
    """ Extracts text from a PDF file.
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        str: The extracted text.
    """
    text = ""
    try:
        # Open the PDF file
        with fitz.open(pdf_path) as doc:
            # Iterate through each page
            for page in doc:
                # Extract text from the page
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_numerical_data(text):
    ph_match = re.findall(r'pH\s*(\d+\.?\d*)', text)
    temp_match = re.findall(r'(\d+\.?\d*)\s*°C', text)
    wavelength_match = re.findall(r'(\d+)\s*nm', text)
    ph_list = [float(ph) for ph in ph_match]
    temp_list = [float(temp) for temp in temp_match]
    wave_list = [float(wave) for wave in wavelength_match]
    return ph_list, temp_list, wave_list
def main():
    text = extract_text_from_pdf("paper_1.pdf")
    ph_list, temp_list, wave_list = extract_numerical_data(text)
    print(ph_list, temp_list, wave_list)


if __name__ == "__main__":
    main()



