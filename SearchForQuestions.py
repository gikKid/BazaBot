from os import write
import docx
import pandas as pd
from docx.api import Document


def iter_unique_cells(row):
    """Generate cells in *row* skipping empty grid cells."""
    prior_tc = None
    for cell in row.cells:
        this_tc = cell._tc
        if this_tc is prior_tc:
            continue
        prior_tc = this_tc
        yield cell

q=[]
a=[]

doc = docx.Document('PandasTableExtraction.docx')
for table in doc.tables:
    for row in table.rows:
        for cell in iter_unique_cells(row):
            for paragraph in cell.paragraphs:
                pass

table = doc.tables[0]

data = []

keys = None
for i, row in enumerate(table.rows):
    text = (cell.text for cell in row.cells)

    if i == 0:
        keys = tuple(text)
        continue
    row_data = dict(zip(keys, text))
    data.append(row_data)
data.to_csv('filename.csv', header = None) 
df = pd.DataFrame(data)

print(df)