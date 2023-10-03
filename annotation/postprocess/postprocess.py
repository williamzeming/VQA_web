import json
from tqdm import tqdm

cate_id_dict = {
    1: 'report_title',
    2: 'form',
    3: 'other',
    4: 'title',
    5: 'paragraph',
    6: 'section',
    7: 'abstract',
    8: 'summary',
    9: 'subsection',
    10: 'subsubsection',
    11: 'table_of_contents',
    12: 'list_of_figures',
    13: 'list_of_tables',
    14: 'figure',
    15: 'figure_caption',
    16: 'table',
    17: 'table_caption',
    18: 'cross',
    19: 'form_title',
    20: 'form_body',
    21: 'list',
    22: 'appendix_list',
    23: 'references',
    24: 'subsubsubsection',
    25: 'subsubsubsubsection'
}


# Extract useful information from merged json file
def import_json(json_filepath):
    """Load json file"""
    with open(json_filepath) as f:
        anno_json = json.load(f)
    return anno_json


def extract_img_info(json_filepath):
    """Extract img info from anno_file into file_json"""
    anno_json = import_json(json_filepath)
    file_json = {}  # define a json file to store bounding box information for each page of a report
    img_id_dict = {}  # define a image id dictionary to store image id and filename for each page of a report
    for img in anno_json['images']:  # image info in anno_json
        img_name = img['file_name']
        file_name = img_name.split('_page-')[0]
        page_id = int(img_name.split('_page-')[1].split('.')[0])
        img_id_dict[img['id']] = img['file_name']
        if file_name not in file_json.keys():
            file_json[file_name] = {}
            file_json[file_name]['page'] = {}
            file_json[file_name]['page'][page_id] = {}
            file_json[file_name]['page'][page_id]['objects'] = {}
            file_json[file_name]['page'][page_id]['width'] = img['width']
            file_json[file_name]['page'][page_id]['height'] = img['height']
            file_json[file_name]['page'][page_id]['category_ids'] = img['category_ids']
            file_json[file_name]['page'][page_id]['dataset_id'] = img['dataset_id']
            file_json[file_name]['page'][page_id]['image_name'] = img['file_name']
            file_json[file_name]['page'][page_id]['image_id'] = img['id']
            file_json[file_name]['page'][page_id]['thumbnail'] = img['regenerate_thumbnail']
            file_json[file_name]['page'][page_id]['box_list'] = []
        else:
            file_json[file_name]['page'][page_id] = {}
            file_json[file_name]['page'][page_id]['objects'] = {}
            file_json[file_name]['page'][page_id]['width'] = img['width']
            file_json[file_name]['page'][page_id]['height'] = img['height']
            file_json[file_name]['page'][page_id]['category_ids'] = img['category_ids']
            file_json[file_name]['page'][page_id]['dataset_id'] = img['dataset_id']
            file_json[file_name]['page'][page_id]['image_name'] = img['file_name']
            file_json[file_name]['page'][page_id]['image_id'] = img['id']
            file_json[file_name]['page'][page_id]['thumbnail'] = img['regenerate_thumbnail']
            file_json[file_name]['page'][page_id]['box_list'] = []
    print('Finished: Extract img info from anno_file into file_json')
    return file_json, img_id_dict


# Reorder the page dictionary keys based on natural page order
def detect_left(bbox, box_list):
    upper_y = bbox[1]
    lower_y = bbox[1] + bbox[3]
    for box in box_list:
        if box != bbox:
            if box[0] < bbox[0] and abs(bbox[0] - box[0]) - box[2] > 0:
                if box[1] + box[3] < upper_y or box[1] > lower_y:
                    continue
                else:
                    return True


def detect_right(bbox, box_list):
    upper_y = bbox[1]
    lower_y = bbox[1] + bbox[3]
    for box in box_list:
        if box != bbox:
            if box[0] > bbox[0] and abs(bbox[0] - box[0]) - bbox[2] > 0:
                if box[1] + box[3] < upper_y or box[1] > lower_y:
                    continue
                else:
                    return True


def y_order(box_list):
    output = []
    box_list.sort(key=lambda x: x[1])
    return box_list


def reading_order(box_list):
    if len(box_list) == 0:
        box = []
        return box
    ordered_list = y_order(box_list)
    result_list = []
    left_box = []
    right_box = []
    for box in ordered_list:
        if detect_left(box, box_list):
            left_box.append(box)
        elif detect_right(box, box_list):
            right_box.append(box)
        else:
            result_list.append(box)
            result_list.extend(reading_order(left_box))
            result_list.extend(reading_order(right_box))
            left_box = []
            right_box = []
    result_list.extend(reading_order(right_box))
    result_list.extend(reading_order(left_box))
    return result_list


def reading_order_id(obj_dict, ro_list):
    ordered_id = []
    ordered_label = []
    for i, box in enumerate(ro_list):
        for obj in obj_dict:
            if obj_dict[obj]['bbox'] == box:
                ordered_id.append(obj)
                ordered_label.append(obj_dict[obj]['category_id'])
        return ordered_id, ordered_label


def implement_reorder(json_filepath):
    """Reordering page dictionary keys based on natural page order"""
    file_json, img_id_dict = extract_img_info(json_filepath)
    new_file_json = {}
    for doc in file_json:
        pages = sorted(file_json[doc]['page'])
        new_file_json[doc] = {}
        new_file_json[doc]['page'] = {}
        for page in pages:
            new_file_json[doc]['page'][page] = file_json[doc]['page'][page]
    return new_file_json


def process_anno_info(json_filepath):
    """Extract annotation info from anno_file into new_file_json and
    Flattening all document component into one list based on reading order"""
    anno_json = import_json(json_filepath)
    file_json, img_id_dict = extract_img_info(json_filepath)
    new_file_json = implement_reorder(json_filepath)
    for objt in anno_json['annotations']:
        img_name = img_id_dict[objt['image_id']]
        file_name = img_name.split('_page-')[0]
        page_id = int(img_name.split('_page-')[1].split('.')[0])
        new_file_json[file_name]['page'][page_id]['box_list'].append(objt['bbox'])
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']] = {}
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['bbox'] = objt['bbox']
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['segmentation'] = objt['segmentation']
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['category_id'] = objt['category_id']
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['category'] = cate_id_dict[objt['category_id']]
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['page'] = page_id
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['relations'] = {}
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['relations']['child'] = []
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['relations']['parent'] = []
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['relations'][
            'above'] = []  # For Cross-page bottom component
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['relations'][
            'following'] = []  # For Cross-page top componet
        new_file_json[file_name]['page'][page_id]['objects'][objt['id']]['relations']['context'] = []

    for doc in new_file_json:
        new_file_json[doc]['components'] = []
        new_file_json[doc]['object_page_list'] = []
        new_file_json[doc]['ordered_id'] = []
        new_file_json[doc]['ordered_label'] = []
        for page in new_file_json[doc]['page']:
            box_list = new_file_json[doc]['page'][page]['box_list']
            ro_list = reading_order(box_list)
            reordered_id, _ = reading_order_id(new_file_json[doc]['page'][page]['objects'], ro_list)
            new_file_json[doc]['page'][page]['reading_order'] = reordered_id
            for objt_id in reordered_id:
                new_file_json[doc]['components'].append(new_file_json[doc]['page'][page]['objects'][objt_id])
                new_file_json[doc]['object_page_list'].append(
                    new_file_json[doc]['page'][page]['objects'][objt_id]['page'])
                new_file_json[doc]['ordered_id'].append(objt_id)
                new_file_json[doc]['ordered_label'].append(
                    new_file_json[doc]['page'][page]['objects'][objt_id]['category'])
    print("""Finished: Extract annotation info from anno_file into new_file_json & Flatening all document component into
     one list based on reading order""")
    return new_file_json


# Append parent-child relationship alignment
def section_paragraph(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']
    for i in range(len(box_id)):
        if box_label[i] in ['section', 'subsection', 'subsubsection', 'subsubsubsection', 'subsubsubsubsection']:
            for j in range(i + 1, len(box_id)):
                if box_label[j] == 'paragraph' or box_label[j] == 'list':
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                elif box_label[j] in ['section', 'subsection', 'subsubsection', 'subsubsubsection',
                                      'subsubsubsubsection']:
                    break


def section_subsection(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']
    for i in range(len(box_id)):
        if box_label[i] == 'section':
            for j in range(i + 1, len(box_id)):
                if box_label[j] == 'subsection':
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                elif box_label[j] in ['section']:
                    break
        if box_label[i] == 'subsection':
            for j in range(i + 1, len(box_id)):
                if box_label[j] == 'subsubsection':
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                elif box_label[j] in ['section', 'subsection']:
                    break
        if box_label[i] == 'subsubsection':
            for j in range(i + 1, len(box_id)):
                if box_label[j] == 'subsubsubsection':
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                elif box_label[j] in ['section', 'subsubsection', 'subsection']:
                    break
        if box_label[i] == 'subsubsubsection':
            for j in range(i + 1, len(box_id)):
                if box_label[j] == 'subsubsubsubsection':
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                elif box_label[j] in ['section', 'subsubsection', 'subsection', 'subsubsubsection']:
                    break


def figure_caption(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']
    for i in range(len(box_id)):
        if box_label[i] == 'figure':
            j = i + 1
            if j < len(box_id) and box_label[j] == 'figure_caption':
                box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                continue
            j = i - 1
            if j >= 0 and box_label[j] == 'figure_caption':
                box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                continue


def table_caption(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']
    for i in range(len(box_id)):
        if box_label[i] == 'table':
            j = i + 1
            if j < len(box_id) and box_label[j] == 'table_caption':
                box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                continue
            j = i - 1
            if j >= 0 and box_label[j] == 'table_caption':
                box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                continue


def form_title_body(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']
    for i in range(len(box_id)):
        if box_label[i] == 'form_title':
            j = i + 1
            if j < len(box_id) and box_label[j] in ['form_body', 'form']:
                box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                continue
            j = i - 1
            if j >= 0 and box_label[j] in ['form_body', 'form']:
                box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                continue


def abstract_summary(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']
    for i in range(len(box_id)):
        if box_label[i] in ['abstract', 'summary']:
            for j in range(i + 1, len(box_id)):
                if box_label[j] in ['paragraph', 'list', 'table', 'table caption', 'figure', 'figure caption', 'form',
                                    'form_body', 'form_title']:
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['child'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['parent'].append(box_id[i])
                elif box_label[j] in ['abstract', 'summary', 'section', 'subsection', 'subsubsection',
                                      'subsubsubsection', 'subsubsubsubsection', 'list_of_tables', 'list_of_tables',
                                      'title', 'appendix_list', 'table_of_contents']:
                    break


def cross_page(box_dict):
    box_id = box_dict['ordered_id']
    box_label = box_dict['ordered_label']
    page_list = box_dict['object_page_list']

    for i in range(len(box_id)):
        if box_label[i] in ['table', 'form']:
            previous_id = i
            for j in range(i + 1, len(box_id)):
                if box_label[j] == 'cross':
                    box_dict['page'][page_list[i]]['objects'][box_id[i]]['relations']['following'].append(box_id[j])
                    box_dict['page'][page_list[j]]['objects'][box_id[j]]['relations']['above'].append(box_id[i])
                    previous_id = j
                else:
                    break


def append_relationship(json_filepath):
    new_file_json = process_anno_info(json_filepath)
    for doc in new_file_json:
        section_paragraph(new_file_json[doc])
        section_subsection(new_file_json[doc])
        figure_caption(new_file_json[doc])
        table_caption(new_file_json[doc])
        form_title_body(new_file_json[doc])
        abstract_summary(new_file_json[doc])
        cross_page(new_file_json[doc])
    print('Finished: Append parent-child relationship')
    return new_file_json


# Associate textline info with objects in a document and sort & organize textlines
def append_textline(json_filepath, textline_folder):
    """Append textline info into pdfminer_textline for each page in every document in new_file_json"""
    problematic_docs = []
    new_file_json = append_relationship(json_filepath)
    for doc in tqdm(new_file_json):  # every document in new_file_json
        for page in new_file_json[doc]['page']:  # every page for every document in new_file_json
            try:
                path = textline_folder + doc + "_page-" + str(page) + ".json"
                with open(path) as f:
                    text_line = json.load(f)  # load textline info
                new_file_json[doc]['page'][page][
                    'pdfminer_textline'] = text_line  # store textline info for each page into new_file_json
            except:
                problematic_docs.append(doc)
    print('Finished: Append textline info into pdfminer_textline for each page in every document')
    print('\n', len(problematic_docs))
    return new_file_json, problematic_docs


def get_intersection_rate(bbox1, bbox2, h):
    bbox1 = [bbox1[0], bbox1[1], bbox1[0] + bbox1[2], bbox1[1] + bbox1[3]]
    bbox2 = [bbox2[0], bbox2[3], bbox2[2], bbox2[1]]
    area1 = (bbox1[3] - bbox1[1]) * (bbox1[2] - bbox1[0])
    area2 = (bbox2[3] - bbox2[1]) * (bbox2[2] - bbox2[0])

    x1 = max(bbox1[0], bbox2[0])
    y1 = max(bbox1[1], bbox2[1])
    x2 = min(bbox1[2], bbox2[2])
    y2 = min(bbox1[3], bbox2[3])

    height = y2 - y1
    width = x2 - x1

    if height <= 0 or width <= 0:
        return 0
    else:
        area = height * width
        # return area / (area1+area2-area)
        return area / area2


def reading_order_id_textline(obj_dict, ro_list):
    ordered_id = []
    ordered_label = []
    for i, box in enumerate(ro_list):
        for obj in obj_dict:
            if box_convertor(obj_dict[obj]['bbox']) == box:
                ordered_id.append(obj)
    return ordered_id, ordered_label


def box_convertor(box):
    new_box = [box[0], box[1], box[2] - box[0], box[3] - box[1]]
    return new_box


def associate_textline(json_filepath, textline_folder):
    new_file_json, problematic_docs = append_textline(json_filepath, textline_folder)
    # A text-line dictionary is created for each object, including a list of sorted text rows, a bounding box,
    # and a list of sorted text rows
    for doc in new_file_json:
        for page in new_file_json[doc]['page']:
            for obj in new_file_json[doc]['page'][page]['objects']:
                objt = new_file_json[doc]['page'][page]['objects'][obj]
                objt['textline'] = {}
                objt['textline']['lines'] = {}
                objt['textline']['bbox'] = []
                objt['textline']['ordered_list'] = []

    # Associate text line information in a PDF document with known objects and try to merge adjacent text lines based
    # on some logic (for example, bounding box crossover rate)
    issue_doc_list = []
    for doc in new_file_json:
        for page in new_file_json[doc]['page']:
            if 'pdfminer_textline' in new_file_json[doc]['page'][page].keys():
                textline = new_file_json[doc]['page'][page]['pdfminer_textline'][doc]
                for line in textline:
                    if 'LTTextBox' in textline[line].keys():
                        bbox_line = textline[line]['LTTextBox']['bbox']
                        text_list = textline[line]['LTTextBox']['text']
                        merged_objt_id = -1
                        rate = 0
                        if text_list == ' \n':
                            continue
                        for obj in new_file_json[doc]['page'][page]['objects']:
                            height = new_file_json[doc]['page'][page]['height']
                            objt = new_file_json[doc]['page'][page]['objects'][obj]
                            if 'textline' not in objt.keys():
                                print(doc)
                            bbox_objt = objt['bbox']
                            new_rate = get_intersection_rate(bbox_objt, bbox_line, height)
                            if new_rate > rate:
                                merged_objt_id = obj
                                rate = new_rate
                        if merged_objt_id != -1:
                            new_file_json[doc]['page'][page]['objects'][merged_objt_id]['textline']['lines'][line] = \
                                textline[line]['LTTextBox']
                            tbbox = textline[line]['LTTextBox']['bbox']
                            textline_bbox = [tbbox[0], tbbox[3], tbbox[2], tbbox[1]]
                            new_file_json[doc]['page'][page]['objects'][merged_objt_id]['textline']['lines'][line][
                                'bbox'] = textline_bbox
                            new_file_json[doc]['page'][page]['objects'][merged_objt_id]['textline']['bbox'].append(
                                textline_bbox)
            else:
                if doc not in issue_doc_list:
                    issue_doc_list.append(doc)

    # Sorts the merged text lines and stores the sorted list of text line ids in the text line information of the object
    for doc in tqdm(new_file_json):
        for page in new_file_json[doc]['page']:
            for obj in new_file_json[doc]['page'][page]['objects']:
                objt = new_file_json[doc]['page'][page]['objects'][obj]
                if objt['category'] in ['table', 'figure']:
                    continue
                line_box_list = objt['textline']['bbox']
                new_line_box_list = []
                for box in line_box_list:
                    new_line_box_list.append(box_convertor(box))
                ro_list = reading_order(new_line_box_list)
                ordered_id, _ = reading_order_id_textline(objt['textline']['lines'], ro_list)
                objt['textline']['ordered_list'] = ordered_id

    # Associate the sorted text line content with an object and store the text content of the text line in the text information of the object
    for doc in tqdm(new_file_json):
        for page in new_file_json[doc]['page']:
            for obj in new_file_json[doc]['page'][page]['objects']:

                objt = new_file_json[doc]['page'][page]['objects'][obj]
                if objt['category'] in ['table', 'figure']:
                    continue
                objt['text'] = ''
                ordered_id = objt['textline']['ordered_list']
                for id in ordered_id:
                    objt['text'] = objt['text'] + ' ' + objt['textline']['lines'][id]['text']
                objt['text'] = objt['text'][1:]
                # print(objt['text'])
    print('All Finished')
    return new_file_json


# Save post-processed json file
def save_json(json_filepath, textline_folder, post_json_filepath):
    new_file_json = associate_textline(json_filepath, textline_folder)
    with open(post_json_filepath, 'w') as f:
        json.dump(new_file_json, f)
