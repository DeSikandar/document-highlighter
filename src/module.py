import pdfplumber
import fitz


def parse_pdf(pdf):
    with pdfplumber.open(pdf) as pdf:
        document_info = dict()
        for i,page in enumerate(pdf.pages):
            word_bboxes = []
            words = page.extract_words()
            for word in words:
                text = word["text"]
                bbox = [word["x0"], word["top"], word["x1"], word["bottom"]]  # Bounding box: (x0, top, x1, bottom)
                word_bboxes.append({"text": text, "bbox": bbox})
                document_info[i] = {"document":word_bboxes, "dimension":[page.width, page.height]}
    pages = i+1
    for j in range(pages):
        # width, height = document_info[j]["dimension"]
        page_document_info = document_info[j]["document"]
        page_document_info_sorted = sorted(page_document_info, key = lambda z:(z["bbox"][1], z["bbox"][0]))
        line_bboxes = group_bboxes_by_lines(page_document_info_sorted)
        formatted_line_bboxes = group_nearest_words(line_bboxes)

        formatted_lines = get_common_bbox_for_neighbors(formatted_line_bboxes)
        extracted_infos = []

        for line in formatted_lines:
            entity = line[0].get('text').split(':')
            if len(entity)>1:
                key_values = {
                    "key": entity[0],
                    "value": entity[1],
                    "highlight_coordinate":line[0]
                }
                extracted_infos.append(key_values)
                
    return extracted_infos

def group_bboxes_by_lines(bboxes, threshold=10):
    grouped_lines = []
    current_line = [bboxes[0]]

    for bbox in bboxes[1:]:
        if abs(bbox["bbox"][1] - current_line[-1]["bbox"][1]) < threshold: #vertical distance 
            current_line.append(bbox)
        else:
            grouped_lines.append(current_line)
            current_line = [bbox]


    grouped_lines.append(current_line)
    return grouped_lines

def group_nearest_words(line_bboxes, h_threshold = 15):
  formatted_line_bboxes = []
  for line in line_bboxes: # boxes in the lines are horizontally sorted
    formatted_line = []
    current_words = [line[0]]

    for i, word in enumerate(line[1:]):

      if abs(word["bbox"][0] - current_words[-1]["bbox"][2]) < h_threshold:
        current_words.append(word)
      else: # mayn't reaches to end words
        formatted_line.append(current_words)
        current_words = [word]

      if i == len(line[1:]) - 1 and current_words not in formatted_line: # if it reaches to end words
        formatted_line.append(current_words)
    formatted_line_bboxes.append(formatted_line)

  return formatted_line_bboxes


def get_common_bbox_for_neighbors(formatted_line_bboxes):
  formatted_lines = []
  for line in formatted_line_bboxes:
    formatted_line = []
    for neighbor_words in line:
      text = neighbor_words[0]["text"]
      x_min, y_min, x_max, y_max = neighbor_words[0]["bbox"]
      if len(neighbor_words) > 1:
        for word in neighbor_words[1:]:
          x1, y1, x2, y2 = word["bbox"]
          # update common bbox
          x_min, y_min = min(x1, x_min), min(y1, y_min)
          x_max, y_max = max(x2, x_max), max(y2, y_max)
          text += " "+ word["text"]
      formatted_line.append({"text":text, "bbox":[x_min, y_min, x_max, y_max]})

    formatted_lines.append(formatted_line)

  return formatted_lines

def add_highlights(page, bbox):
  rectangle = fitz.Rect(bbox)
  highlight = page.add_highlight_annot(rectangle)
  highlight.set_colors({"stroke": (1, 1, 0)})

  return page

def save_highlight_pdf(pdf_file,output_file,page_num, extracted_info):
  # Create a PDF document object
  pdf_document = fitz.open(pdf_file)
  # Get the page you want to work with (for example, page index 0)
  page = pdf_document[page_num]


  # loop over each eactracted info
  # print(extracted_info['bbox']) 
  bbox = extracted_info['bbox']
  add_highlights(page, bbox)
  
  # for key_value_pairs in extracted_info:
  #   key_bbox = key_value_pairs["highlight_coordinate"]["bbox"]
  #   keys_highlighted_page = add_highlights(page, key_bbox)


  # Update the PDF with the new annotation
  pdf_document.save(output_file)

  # Close the PDF document
  pdf_document.close()

