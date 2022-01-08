#from typing_extensions import runtime
import docx
import json
import io
import docx
from docx.shared import RGBColor
import random

def get_json(doc,user_name):
    doc = docx.Document(f"{doc}") #документ базы
    table = doc.tables[0]

    data = []
    result = []
    keys = None

    for table in doc.tables:
        table
        for i, row in enumerate(table.rows):
            text = (cell.text for cell in row.cells)

            if i == 0:
                keys = tuple(text)
                continue
            row_data = dict(zip(keys, text))
            data.append(row_data)

    for table in doc.tables:
        for row in table.rows:
            j = 0
            for cell in row.cells:
                j+= 1
                if len(data[1]) == 2:
                    if j == 1:
                        array = []
                        array.append(cell.text)
                elif len(data[1]) == 3:
                    if j == 1:
                        array = []
                        array.append(cell.text)
                    elif j == 2:
                        array.append(cell.text)
                for para in cell.paragraphs:
                    for run in para.runs:                
                        check = RGBColor.from_string('FF0000')
                        if run.font.color.rgb == check :
                            if run.text != " " and run.text != "\n":
                                text1 = para.text
                                text_array = []
                                if len(data[1]) == 2:
                                    text_array.append(array[0])
                                    text_array.append(text1)
                                elif len(data[1]) == 3:
                                    text_array.append(array[0])
                                    text_array.append(array[1])
                                    text_array.append(text1)
                                row_data = dict(zip(keys, text_array))
                                result.append(row_data)

    seen = set()
    new_result = []
    for d in result:
        t = tuple(sorted(d.items()))
        if t not in seen:
            seen.add(t)
            new_result.append(d)
    for d in data:
        for n in new_result:
            if list(n.items())[0][1] == list(d.items())[0][1]: # защита от долбаебов
                d["Ответ"] = list(n.items())[1][1]

    with io.open(f"table{user_name}.json", "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4, ensure_ascii=False)

def shuf(user_name):
    with io.open(f"table{user_name}.json", encoding="utf-8") as f:
        templates = json.load(f) #чтение json файла в list
    random.shuffle(templates)
    with io.open(f"table{user_name}shuf.json", "w", encoding="utf-8") as data_file:
        json.dump(templates, data_file, indent=4, ensure_ascii=False) #сохранение нового json файла с перемешанными данными
