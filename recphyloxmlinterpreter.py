#recphyloxmlinterpreter
#Garrett Chappell, Summer 2021
#Call script with:
#			python recphyloxmlinterpreter.py [events summary file] [node names with dates file] [recPhyloXML file]
#Function:
#Takes in the events summary file from recPhyloXMLEventSummary.py, a file that has the internal node names from the chronogram and dates, and the recPhyloXML file, and gives a midpoint date for each gene event
#NOTE: Before using the events summary file, all of the spaces between columns need to be replaced with a single tab between each column


import sys
import ete3
from ete3 import Phyloxml
import tempfile
infile1 = sys.argv[1]
infile2 = sys.argv[2]
infile3 = sys.argv[3]
eventFile = open(infile1)
xmlFile = open(infile3)


#Writing a temporary file with the species tree from the recPhyloXML file
speciesXML = tempfile.NamedTemporaryFile()
lineNum = 0
xmlLines =[]
for line in xmlFile:
	lineNum += 1
	xmlLines.append(line)
	if '<spTree>' in line:
		firstLine = lineNum
	if '</spTree>' in line:
		lastLine = lineNum
if '<recGeneTree>' in xmlLines[lastLine - 1]:
	xmlLines[lastLine - 1] = xmlLines[lastLine - 1].replace('<recGeneTree>', '')
for i in range(firstLine - 1, lastLine):
	speciesXML.write(str(xmlLines[i]))


#Using the temporary species tree file to create a tree using ete3
speciesXML.seek(0)
project = Phyloxml()
project.build_from_file(speciesXML)


#Creating dictionary of child nodes and their parent node
parentDict = {}
for tree in project.get_phylogeny():
	for node in tree.iter_descendants("postorder"):
		parentDict[node.name] = tree.get_common_ancestor(node, node.get_sisters()[0].name).name


#Setting up the created output file
outfile = open(str(infile1 + '_event_dates.txt'), 'w')
outfile.write('event	left node	right node	left date	right date	midpoint date' + '\n')


##Creating dictionary of node names and their age from the input file
nodeDict = {}
nodeFile = open(infile2, 'r')
nodeLines = nodeFile.readlines()[1:]
for line in nodeLines:
	cols = line.split('\t')
	nodeName = cols[0]
	avgDate = cols[3].strip()
	nodeDict[nodeName] = avgDate


#Extracting the data from the event summary input file
eventLines = eventFile.readlines()[1:]
for line in eventLines:
	columns = line.split('\t')
	rightNode = str(columns[0]) #gets name of right node
	numDup = int(columns[1]) #gets number of duplications on that branch
	numLos = int(columns[2]) #gets number of losses on that branch
	numTrD = int(columns[3]) #gets number of transfer departures on that branch (unused)
	numTrR = int(columns[4]) #gets number of transfer receptions on that branch


	#Determining what the left node (parent node) is given the right node
	if rightNode in parentDict:
		leftNode = parentDict[rightNode]
	else:
		leftNode = '?'
	

	#Determining the date for the left node (parent node)
	if leftNode in nodeDict:
		leftDate = float(nodeDict[leftNode])
	else:
		leftDate = '?'


	#Determining the date for the right node
	if rightNode in nodeDict:
		rightDate = float(nodeDict[rightNode])
	else:
		rightDate = 0.0 #This is a leaf (today)


	#Calculating the midpoint date of the event
	if type(leftDate) == float and type(rightDate) == float:
		midpointDate = (leftDate + rightDate) / 2
	else:
		midpointDate = '?'
	

	#Writing the lines for the duplication events on this branch
	for i in range(numDup):
		outfile.write('dup' + '\t' + str(leftNode) + '\t' + str(rightNode) + '\t' + str(leftDate) + '\t' + str(rightDate) + '\t' + str(midpointDate) + '\n')


	#Writing the lines for the loss events on this branch
	for i in range(numLos):
		outfile.write('los' + '\t' + str(leftNode) + '\t' + str(rightNode) + '\t' + str(leftDate) + '\t' + str(rightDate) + '\t' + str(midpointDate) + '\n')


	#Writing the lines for the transfer events on this branch (only using transfer receptions)
	for i in range(numTrR):
		outfile.write('hgt' + '\t' + str(leftNode) + '\t' + str(rightNode) + '\t' + str(leftDate) + '\t' + str(rightDate) + '\t' + str(midpointDate) + '\n')


#Closing files
nodeFile.close()
eventFile.close()
outfile.close()
speciesXML.close()
xmlFile.close()

