#getGeneBirthDate
#Garrett Chappell, Summer 2021
#Call script with:
#			python getGeneBirthDate.py [symmetric.events_event_dates.txt file]
#Function:
#Prints the midpoint date and date range for the earliest event identified by ecceTERA, assuming this earliest event is close to the birth of the gene


import sys
infile1 = sys.argv[1]
eventFile = open(infile1)


#Creating a list of all the midpoint dates
midList = []
eventLines = eventFile.readlines()[1:]
for line in eventLines:
	columns = line.split('\t')
	midList.append(columns[5].strip())
for item in midList:
	if item != '?':
		midList[midList.index(item)] = float(item)


#Finding the oldest date
oldDate = 0.0
for item in midList:
	if item != '?':
		item = float(item)
		if item > oldDate:
			oldDate = item 


#Finding and printing the data associated with the oldest date
lineIndex = midList.index(oldDate)
lineData = eventLines[lineIndex].split('\t')
lineData[5] = lineData[5].strip()
#print(lineData)
print("Event Type: " + str(lineData[0]))
#print("Left Node: " + str(lineData[1]))
#print("Right Node: " + str(lineData[2]))
print("Range: " + str(lineData[4]) + " - " + str(lineData[3]))
print("Midpoint Date: " + str(lineData[5]))


#Closing files
eventFile.close()
