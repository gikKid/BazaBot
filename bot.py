# http api: 5095964171:AAH0en9UsoV5YU0uR1mSYoGpUKMQOwshUW8
# юкаса токен:  381764678:TEST:32196

import pandas as pd
from docx import Document

document = Document("PandasTableExtractioncopy.docx")

df_tables = []
for table in document.tables:
    df = [['' for i in range(len(table.columns))] for j in range(len(table.rows))]
    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            if cell.text:
                df[i][j] = cell.text
    df_tables.append(pd.DataFrame(df))

print(df_tables)