import math, re, string
from datetime import datetime

# for data with a column containing ticker for milliseconds
def downsample(data, targetRate, tickerColumn = 1):
	ind = 1
	result = [[0] * len(data[0]) for i in range( int(float(data[-1][tickerColumn])/targetRate) )]
	for x in range(1,int(float(data[-1][tickerColumn])/targetRate)):
		index = getNextIndex(data, x*(1000/targetRate), ind)
		ind = index[0]
		for col in range(len(data[x])):
			if col == tickerColumn:
				result[x][col] = x*(1000/targetRate)
			else:
				if index[1] == 1 or re.search( ':', data[ind][col]):
					result[x][col] = data[ind][col]
				else:
					if len(data[ind-1][col]) > 0 and len(data[ind][col]) > 0:
						percentage = ( x*(1000/targetRate) - float(data[ind-1][tickerColumn]) ) / ( float(data[ind][tickerColumn]) - float(data[ind-1][tickerColumn]) )
						result[x][col] = float(data[ind-1][col].replace(',', '.')) * percentage + float(data[ind-1][col].replace(',', '.')) * (1-percentage)
	return result


# helper function for downsample
# gets the index of the element of data with the higher millisecond value in its ticker column
def getNextIndex(data, position, searchFrom = 1, tickerColumn = 1):
	found = searchFrom
	while position > float(data[found][tickerColumn]) and found < len(data):
		found += 1
	return [found, 1 if position == float(data[found][tickerColumn]) else 0]


# used to complete the dataset by calculating average values of the neigbor elements for the accelerometer where the values are missing
def completeDataSet(data, column, tickerColumn = 1):
	for x in range(0,len(data)-1):
		data[x+1][column] = data[x+1][column].replace(',', '.')
		if data[x][column] == '':
			if x > 0 and len(data[x-1][column]) > 0 and len(data[x+1][column]) > 0:
				percentage = (float(data[x][tickerColumn])-float(data[x-1][tickerColumn])) / ((float(data[x+1][tickerColumn])-float(data[x-1][tickerColumn])))
				data[x][column] = str((float(data[x-1][column]) * percentage + float(data[x+1][column]) * (1-percentage)))


# helper function for completeDataSet
# not yet finished or implemented
# searches for the next valid data in a given column in the data, from the start position, in direction 1 or -1
#def searchNextVal(data, start, column, direction = 1):
#	x = start
#	while x > 0 and x < len(data):
#		if len(data[x][column]) > 0:
#			return x-start


# used to select only certain columns from the data. Specified by the integer list 'columns'
# data is a list of strings, and the columns are separated by 'delimiter' (by default a tab)
def selectData(data, columns, delimiter = '\t'):
	result = [[0] * len(columns) for i in range(len(data))]
	for x in range(0,len(data)):
		temp = data[x].split(delimiter)
		for y in range(0,len(columns)):
			result[x][y] = temp[columns[y]]
	return result


# used to open a tsv file and return the contents as line strings
def openTSV(path):
	if len(path) > 0:
		theFile = open(path,'r', encoding='utf-16-le')
		content = theFile.readlines()
		theFile.close()
		return content
	return []


# returns the square root of the sum of the squares of the components in componentList
def pyth(componentList):
	sum = 0
	for x in range(0,len(componentList)):
		sum += float(componentList[x]) * float(componentList[x])
	return math.sqrt(sum)



# testcode (remove if it interferes)

temp = selectData(openTSV("./ToolDev/Sampel Rec01/Eye-tracking/Rec2.tsv"), [2,3,4,5,7,8,9])

for i in range(4,6+1):
	completeDataSet(temp, i)

temp = downsample(temp, 32)


#print(temp[11][4])

for x in range(0,len(temp)):
#	print(temp[x])
	print(pyth([temp[x][4],temp[x][5],temp[x][6]]))


