import pandas as pd
import numpy as np
import lz4.frame

def file_loader(name_file):

    chunk_size = 128 * 1024 * 1024
    with lz4.frame.open(name_file, 'r') as file:
        chunk = file.read(size=chunk_size).decode('utf-8').splitlines()

    data = []
    for row in chunk:
        data.append(row.split(","))

    df = pd.DataFrame(data[1:], columns = data[0])
    
    return df

def data_types_converter(df, cols):
    
    for col in cols:
        try:
            df[col] = df[col].astype(float)
#             print(col, "converted to float")
        except:
#             print(col, "not converted to float")
            pass;
    
    return df