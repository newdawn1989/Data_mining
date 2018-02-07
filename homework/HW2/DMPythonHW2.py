#Assignment based on http://www.nasdaq.com/quotes/
#Feel free to use any libraries. 
#Make sure that the output format is perfect as mentioned in the problem.
#Also check the second row of the download dataset.
#If it follows a different format, avoid it or remove it.
'''
Sources:
https://stackoverflow.com/questions/35091879/merge-2-arrays-vertical-to-tuple-numpy
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html
https://stackoverflow.com/questions/19486369/extract-csv-file-specific-columns-to-list-in-python/19487003
https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module
https://pyformat.info/
https://stackoverflow.com/questions/6081008/dump-a-numpy-array-into-a-csv-file
https://docs.python.org/2/library/csv.html
https://pymotw.com/2/csv/
'''
import argparse
import numpy as np
import csv
import pandas as pd
import sys
from scipy import stats
from scipy.stats.stats import pearsonr 

def readData(fileName, attribute):
	'''
class csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
Create an object which operates like a regular reader but maps the information read into a dict whose keys 
are given by the optional fieldnames parameter. The fieldnames parameter is a sequence whose elements are 
associated with the fields of the input data in order. These elements become the keys of the resulting dictionary. 
If the fieldnames parameter is omitted, the values in the first row of the csvfile will be used as the fieldnames. 
If the row read has more fields than the fieldnames sequence, the remaining data is added as a sequence keyed by the 
value of restkey. If the row read has fewer fields than the fieldnames sequence, the remaining keys take the value of the 
optional restval parameter. Any other optional or keyword arguments are passed to the underlying reader instance.
A short usage example:
>>> import csv
>>> with open('names.csv') as csvfile:
...     reader = csv.DictReader(csvfile)
...     for row in reader:
...         print(row['first_name'], row['last_name'])
...
Baked Beans
Lovely Spam
Wonderful Spam
https://docs.python.org/2/library/csv.html
	'''
	'''
	command_line_input = sys.argv[4]# parsing commandline input to get the desired attribute
	f = open(fileName, 'r')#open csv file
	df = pd.read_csv(f)#read in csv file
	reader= df[str(command_line_input)]#parseing command line input
	colnames = [command_line_input]#get attributes into list
	colnames = ''.join(colnames)
	print colnames
	attr_val = df[colnames].tolist()#selecting column of csv file based on attribute and converting to a list
	f.close()# close file c2q
	'''
	attr_val = []
	with open(fileName, 'r') as in_file:#opens the file
		reader = csv.DictReader(in_file)#uses DictReader, see above documentation, to isolate columns
		for row in reader:
			if attribute in row:#checks for the attribute
				value = float((row[attribute]))#converts the row-th val to a float
				attr_val.append(value)#append the float val to our list
	in_file.close()#close the in_file
	return attr_val
	

def min_max(values_to_norm):

	min_val = min(values_to_norm)# get the min float val from our list of values
	max_val = max(values_to_norm)#get the max float val from our list of values
	#values to scale min_max calculation to any range, not jsut 0 - 1.0
	new_min = 0.0
	new_max = 1.0
	origional_and_normalized = []#list to store the origional value and the normalized values as a tuple
	for value in values_to_norm:#normalizing the values using the min/max formupa for a 0-1 scale
		min_max_val = ((value-min_val)/(max_val-min_val))*(new_max-new_min)+new_min
		origional_and_normalized.append((value, min_max_val))
	return origional_and_normalized
	
def z_score(values_to_norm):
	#Z-score: The distance between the raw score and the population mean in the unit of the standard deviation
	z_values = stats.zscore(values_to_norm)# uses python library stats and the method zscore to calcualte the z score
										   # for the values in our dataset .
	origional_and_normalized = zip(values_to_norm, z_values)# zips our pre-normalized values and our z_score values into a list

	return origional_and_normalized


def normalization ( fileName , normalizationType , attribute):
    values_to_norm = readData(fileName, attribute)
    if normalizationType=='min_max':
    	values_to_norm = min_max(values_to_norm)
    elif normalizationType == 'z_score':
    	values_to_norm = z_score(values_to_norm)

    for val in values_to_norm:
    	print'Original attribute: {0}\t Normalized value: {1}'.format(val[0], val[1])

def correlation ( attribute1 , fileName1 , attribute2, fileName2 ):
	'''
	(b) Given two filenames, their corresponding attribute types, compute the correlation coefficient between the 
	two attributes types in the two files. Output a single value, which is the correlation coefficient. 
	'''
	#reads in both input files and calles reaadData on them to isolate the given column of
	#a specified attribute
	input_1 = readData(fileName1, attribute1)
	input_2 = readData(fileName2, attribute2)
  	#calles numpy corrcoef to calcuate the corrilation correficient between the inputs
	
	try:
		corrilation_coefficient =  np.corrcoef(input_1, input_2)
		print corrilation_coefficient[0,1]
	except ZeroDivisionError: 
		print "Divide by 0 error"
	




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Mining HW2')
    parser.add_argument('-f1', type=str,
                            help="Location of filename1. Use only f1 when working with only one file.",
                            required=True)
    parser.add_argument("-f2", type=str, 
                            help="Location of filename2. To be used only when there are two files to be compared.",
                            required=False)
    parser.add_argument("-n", type=str, 
                            help="Type of Normalization. Select either min_max or z_score",
                            choices=['min_max','z_score'],
                            required=False)
    parser.add_argument("-a1", type=str, 
                            help="Type of Attribute for filename1. Select either open or high or low or close or volume",
                            choices=['open','high','low','close','volume'],
                            required=False)
    parser.add_argument("-a2", type=str, 
                            help="Type of Attribute for filename2. Select either open or high or low or close or volume",
                            choices=['open','high','low','close','volume'],
                            required=False)



    args = parser.parse_args()

    if ( args.n and args.a1 ):
        normalization( args.f1 , args.n , args.a1 )
    elif ( args.f2 and args.a1 and args.a2):
        correlation ( args.a1 , args.f1 , args.a2 , args.f2 )
    else:
        print "Kindly provide input of the following form:\nDMPythonHW2.py -f1 <filename1> -a1 <attribute> -n <normalizationType> \nDMPythonHW2.py -f1 <filename1> -a1 <attribute> -f2 <filename2> -a2 <attribute>"
