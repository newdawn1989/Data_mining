#!/usr/bin/env python

import sys
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 



#used to give data headers string value 1-10 to access based on command line input
#df = pd.read_csv('magic04.data.csv') 
#df.columns = ['1','2','3','4','5','6','7','8','9','10','11']
#df.to_csv('magic04.data_1.csv')

command_line_input = sys.argv[1]
df = pd.read_csv('magic04.data_1.csv')
 #df['ith column']


#do calculating IQRgit
q1 = df[str(command_line_input)].quantile(.25)
q3 = df[str(command_line_input)].quantile(.75)
iqr = q3-q1

#converting contents of df to a list of ints
#then appending the iqp to that list
#then converting that list of ints to a str
myList=[]
new_df=df[str(command_line_input)].describe()
for i in range(0,8):
	myList.append(new_df[i])
myList.append(iqr)
str1 = ' '.join(str(i) for i in myList)
print str1


#creating scatterplot of attributes 4 and 5
plt.title('Attribute 4 vs Attribute 5')
plt.xlabel('Attribute 4')
plt.ylabel('Attribute 5')
x = df['4']
y = df['5']
graph = plt.scatter(x,y)
plt.show(graph)
