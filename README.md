# document-highlighter

Use NLP for the text Highlighting with spaCy
SpaCy have pre-train model for the NLP so using this we will get the Named Entity Recognition (NER) and using NER we will mark the word or sentence highlighted

With using NLP approach we can achieve the High accuracy but need to download pre-train model and may be computationally expensive.

For the document viewer i have use the simple html for now in the html we can easily highlight the selected text

i have also try with pdfjs library but there are some module is outdated  for that library for the highlight the text like TextLayerBuilder to extract the full text so we can use the pdfjs for the view purpose only there are some good library Adobe PDF Embed API, PDF.js Express but this are paid library but it will support the highlighting we can pass the NER in that library as array and get highlighted text


i have also include the TestPA.pdf file that i am using for the testing 


# install pipenv 
pip install pipenv

# install dependency
pipenv shell 
pipenv install 
python -m spacy download en_core_web_sm

# run the app 
python src/main.py

# step for process the file

once app is started navigate to http://127.0.0.1:5000
and upload pdf file there and hit Submit btn and you get the highlighted view of the document 
