import pandas as pd
import numpy as np
df = pd.read_csv('E:\\Temp\\Selecting_Subs\\Jupyter Notebooks\\data\\sample_data.csv', index_col=0)
print(df, end='\n\n')
print(df.index)
print(df.columns)
print(df.values, end='\n\n')
print(type(df.index))
print(type(df.columns))
print(type(df.values), end='\n\n')
print(df['food'], end='\n\n') # 直接将列名传递给它, 选择一个列作为series
print(df[['food']], end='\n\n') # 将列表传递给它, 选择多个列作为DataFrame
print(df[['height', 'color']], end='\n\n')
print(df.loc['Niko'], end='\n\n') # 返回一行作为series
print(df.loc[['Niko']], end='\n\n')
print(df.loc[['Niko', 'Penelope']], end='\n\n')
print(df.loc['Niko': 'Dean'], end='\n\n')  # 切片
print(df.loc[: 'Aaron'], end='\n\n')
print(df.loc['Niko': 'Christina': 2], end='\n\n')
print(df.loc['Dean':], end='\n\n')
print(df.loc[['Dean', 'Cornelia'], ['age', 'state', 'score']], end='\n\n')  # df.loc[行, 列]
print(df.loc[['Dean', 'Aaron'], 'food'], end='\n\n')
print(df.loc['Jane': 'Penelope', ['state', 'color']], end='\n\n')
print(df.loc['Jane', 'age'], end='\n\n')
print(df.loc[: 'Dean', 'height':], end='\n\n')
print(df.loc[:, ['food', 'color']], end='\n\n')
print(df.loc[['Penelope', 'Cornelia'], :], end='\n\n')
print(df.loc[['Penelope', 'Cornelia']], end='\n\n')
rows = ['Jane', 'Niko', 'Dean', 'Penelope', 'Christina']
cols = ['state', 'age', 'height', 'score']
print(df.loc[rows, cols], end='\n\n')

print(df.iloc[3], end='\n\n')
print(df.iloc[[5, 2, 4]], end='\n\n')
print(df.iloc[3: 5], end='\n\n')
print(df.iloc[3:], end='\n\n')
print(df.iloc[3:: 2], end='\n\n')
print(df.iloc[[2, 3], [0, 4]], end='\n\n')
print(df.iloc[3: 6, [1, 4]], end='\n\n')
print(df.iloc[2: 5, 2: 5], end='\n\n')
print(df.iloc[0, 2], end='\n\n')
print(df.iloc[:, 5], end='\n\n')

food = df['food']
print(food.loc['Aaron'], end='\n\n')
print(food.loc[['Dean', 'Niko', 'Cornelia']], end='\n\n')
print(food.loc['Niko': 'Christina'], end='\n\n')
print(food.loc[['Aaron']], end='\n\n')

print(food.iloc[[4, 1, 3]], end='\n\n')
print(food.iloc[4: 6], end='\n\n')

print(df.state, end='\n\n')
print(df.age, end='\n\n')

print(df[['age', 'age', 'age']], end='\n\n')
