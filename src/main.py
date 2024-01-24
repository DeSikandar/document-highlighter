from flask import Flask, render_template, request
import spacy
import PyPDF2
import re
import base64


app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/highlight',methods=['POST'])
def get_heigh_lighted():
    pdf_file = request.files['pdfFile']
    document_text = extract_text_from_pdf(pdf_file)
    patientAge = request.form['patientAge']
    patientName = request.form['patientName']
    doc = nlp(document_text)
    #disable the nlp to get the entity for the getting the custom input 
    # extracted_entities = [ent.text for ent in doc.ents]
    extracted_entities = [patientAge,patientName]
    # Highlight extracted entities
    highlighted_document = highlight_text(document_text, extracted_entities)
    return render_template('result.html', highlighted_document=highlighted_document)
    
    
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text

def highlight_text(document, entities):
    highlighted_document = document
    for entity in entities:
        highlighted_document = re.sub(r'\b' + re.escape(entity) + r'\b', 
                                      f'<span class="highlight">{entity}</span>', 
                                      highlighted_document, flags=re.IGNORECASE)
    return highlighted_document
    

if __name__ == '__main__':
    app.run(debug=True)