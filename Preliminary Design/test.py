import numpy as np
import pandas as pd
file = "Preliminary Design\Preliminary design.xlsx"
sheet_name1 = "Sheet3"

a = np.array([[1, 2], [3, 4]])

b = np.array([[5, 6]])

print(np.concatenate((a, b), axis=0))

result = np.concatenate((a, b.T), axis=1)

df = pd.DataFrame(result, columns = None, index = None)
print (df)

df.to_excel(file, sheet_name = sheet_name1)  


