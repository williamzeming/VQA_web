import json
import os
import cv2
import fitz
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTFigure
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage



def get_bbox(sizeRatioW, sizeRatioH, pageW, pageH, bbox):
    return int(bbox[0] * sizeRatioW), int(pageH - bbox[1] * sizeRatioH), int(bbox[2] * sizeRatioW), int(
        pageH - bbox[3] * sizeRatioH)


def pdftoimg(filepath, imgpath):
    """
    Transform PDF file to images.

    filepath: pdf file path
    imgpath: folder path to store images
    """
    doc = fitz.open(filepath)
    i = 0
    pdfname = os.path.basename(filepath).split('.')[0]
    # pdfname = filepath.split('.')[0].split('/')[-1]
    print(pdfname)
    for page in doc:
        i += 1
        pix = page.get_pixmap()
        img_name = "{}_page-{}.png".format(pdfname, page.number)
        pix.save(os.path.join(imgpath, img_name))


def preprocess(doc_path):
    """
    Extract text line information from PDF.
    doc_path: path of PDF that need to preprocess
    """

    todo_file = doc_path.split('/')[-1]
    file_name = todo_file[:-4]

    img_textlines = './annotation/preprocess/img_textline/' + file_name + '/'
    img_with_bbox = './annotation/preprocess/img_with_bbox/' + file_name + '/'
    img_without_bbox = './annotation/preprocess/img_without_bbox/' + file_name + '/'
    # Ensure directories exist
    os.makedirs(img_textlines, exist_ok=True)
    os.makedirs(img_with_bbox, exist_ok=True)
    os.makedirs(img_without_bbox, exist_ok=True)

    # Store images to img_without_bbox folder
    pdftoimg(doc_path, img_without_bbox)

    document = open(doc_path, 'rb')
    # Create resource manager
    rsrcmgr = PDFResourceManager()
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_num = 0

    try:
        for page in PDFPage.get_pages(document):

            json_file = {file_name: {}}

            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = device.get_result()
            obj_id = 0

            imgFilePath = img_without_bbox + file_name + '_page-' + str(page_num) + '.png'

            img = cv2.imread(imgFilePath, cv2.IMREAD_UNCHANGED)

            imgHeight, imgWidth, imgChannels = img.shape

            pageW = page.mediabox[2]
            pageH = page.mediabox[3]
            sizeRatioW = imgWidth / page.mediabox[2]
            sizeRatioH = imgHeight / page.mediabox[3]

            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox):
                    for obj in lt_obj:
                        new_bbox = get_bbox(sizeRatioW, sizeRatioH, pageW, pageH, obj.bbox)  # find text box
                        cv2.rectangle(img, (new_bbox[0], new_bbox[1]), (new_bbox[2], new_bbox[3]), (0, 0, 255, 255),
                                      1)  # red
                        if obj_id not in json_file[file_name]:
                            json_file[file_name][obj_id] = {}
                            json_file[file_name][obj_id]['LTTextBox'] = {}
                            json_file[file_name][obj_id]['LTTextBox']['bbox'] = new_bbox
                            json_file[file_name][obj_id]['LTTextBox']['text'] = obj.get_text()
                            obj_id += 1

                elif isinstance(lt_obj, LTFigure):
                    for obj in lt_obj:
                        new_bbox = get_bbox(sizeRatioW, sizeRatioH, pageW, pageH, obj.bbox)  # find text box
                        cv2.rectangle(img, (new_bbox[0], new_bbox[1]), (new_bbox[2], new_bbox[3]), (0, 255, 0, 255),
                                      1)  # green
                        if obj_id not in json_file[file_name]:
                            json_file[file_name][obj_id] = {}
                            json_file[file_name][obj_id]['LTFigure'] = {}
                            json_file[file_name][obj_id]['LTFigure']['bbox'] = new_bbox
                            obj_id += 1

            # save img
            img_file = img_with_bbox + file_name + '_page-' + str(page_num) + '.png'
            cv2.imwrite(img_file, img)

            file_loc = img_textlines + file_name + file_name + "_page-" + str(page_num) + ".json"

            with open(file_loc, 'w') as output:
                json_str = json.dumps(json_file)
                output.write(json_str)

            page_num += 1
    except Exception as e:
        print(f'The file {todo_file} cannot extract textline information. Please try another file.')

