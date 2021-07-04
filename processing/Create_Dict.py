# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:53:22 2020

@author: Work Station
"""

import pandas as pd

with open('text.txt', 'r') as f:
    species = f.readlines()

df = pd.DataFrame(species, columns=['All'])

df = df[df['All'] != ' ENGLISH NAME 4-LETTER CODE SCIENTIFIC NAME 6-LETTER CODE\n']
df.reset_index(drop=True, inplace=True)
df['All'] = df['All'].apply(lambda x: x.replace('*','').replace('\n',''))
df['SpeciesName'] = df['All'].apply(lambda x: x.split(' ')[0:-3])
for i in reversed(range(len(df.SpeciesName))):
    if '+' in df['SpeciesName'][i]:
        df = df.drop(df.index[i])
    else:
        pass
df.reset_index(drop=True, inplace=True)
df['FirstName'] = df['SpeciesName'].apply(lambda x: ' '.join(x[0:2]) if len(x)==4 else x[0])
for row in range(len(df)):
    x = df['SpeciesName'][row]
    if len(x)==2:
        df.at[row, 'SecondName']=''
    elif len(x)==3:
        df.at[row, 'SecondName']=x[1]
    elif len(x)==4:
        df.at[row, 'SecondName']=x[2]
    else:
        pass
df['4-LetterCode'] = df['SpeciesName'].apply(lambda x: x[-1])
df.drop('All', axis=1, inplace=True)
df.drop('SpeciesName', axis=1, inplace=True)
df.to_csv('SpeciesCodes.csv', index=False)


