from flask import Flask, render_template, request
import spacy
import PyPDF2
import re
import base64
import ast
from module import parse_pdf,save_highlight_pdf
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# nlp = spacy.load("en_core_web_sm")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/highlight',methods=['POST'])
def get_heigh_lighted():
    pdf_file = request.files['pdfFile']
    
    
    ext = parse_pdf(pdf_file)
    out_put_file = os.path.join(app.root_path, 'static', 'highlight.pdf')
    
    pdf_file.stream.seek(0)
    original_file = os.path.join(app.root_path,'static','original.pdf')
    pdf_file.save(original_file)
    # save_highlight_pdf(pdf_file=pdf_file.stream,output_file=out_put_file,page_num=0,extracted_info=ext,type=pdf_file.content_type)
    return render_template('result.html',extract_info = ext,original_file=original_file)
    
    
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text

@app.route('/get-highlight',methods=['POST'])
def get_high_lighted():
    data = request.form['data']
    dict = ast.literal_eval(data)
    original_file = os.path.join(app.root_path,'static','original.pdf')
    out_put_file = os.path.join(app.root_path, 'static', 'highlight.pdf')
    print(dict)
    save_highlight_pdf(pdf_file=original_file,output_file=out_put_file,page_num=0,extracted_info=dict)
    return 'done'

def highlight_text(document, entities):
    highlighted_document = document
    for entity in entities:
        highlighted_document = re.sub(r'\b' + re.escape(entity) + r'\b', 
                                      f'<span class="highlight">{entity}</span>', 
                                      highlighted_document, flags=re.IGNORECASE)
    return highlighted_document
    

if __name__ == '__main__':
    app.run(debug=True)