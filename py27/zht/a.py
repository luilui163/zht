#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
df1 = pd.DataFrame( {
    "Name" : ["Alice", "Bob", "Mallory", "Mallory", "Bob" , "Mallory"] ,
    "City" : ["Seattle", "Seattle", "Portland", "Seattle", "Seattle", "Portland"] } )

g1=df1.groupby(['Name','City']).count()

g1.add_suffix('_count').reset_index()