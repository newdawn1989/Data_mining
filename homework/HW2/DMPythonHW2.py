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

def readData(fileName, attribute):
	command_line_input = sys.argv[4]# parsing commandline input to get the desired attribute
	f = open(fileName, 'r')#open csv file
	df = pd.read_csv(f)#read in csv file
	reader= df[str(command_line_input)]#parseing command line input
	colnames = [command_line_input]#get attributes into lisst
	attr_val = df.high.tolist()#selecting column of csv file based on attribute and converting to a list
	f.close()# close file c2q
	return attr_val
	

def min_max(values_to_norm):
	#USE FORULA FROM LECTURE SLIDES!!!
	#formula for normalizing on a scale of 0-1 is (x-min)/(max-min)
	min_val = min(values_to_norm)# get the min float val from our list of values
	max_val = max(values_to_norm)#get the max float val from our list of values
	origional_and_normalized = []#list to store the origional value and the normalized values as a tuple
	for value in values_to_norm:#normalizing the values using the min/max formupa for a 0-1 scale
		min_max_val = ((value-min_val)/(max_val-min_val))
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
    Input Parameters:
        attribute1: The attribute you want to consider from file1
        attribute2: The attribute you want to consider from file2
        fileName1: The comma seperated file1
        fileName2: The comma seperated file2
        
    Output:
        Print the correlation coefficient 
    '''
    #TODO: Write code given the Input / Output Paramters.

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
