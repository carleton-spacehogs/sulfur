#getInternalNodeDates
#Garrett Chappell, Summer 2021
#Call script with:
#			python getInternalNodeDates.py [chronogram] [recPhyloXML file]
#Function:
#Takes in the chronogram and the recPhyloXML file and outputs a file that has the internal node names from the recPhyloXML file and dates from the chronogram for each internal node


import sys
import ete3
from ete3 import Tree, Phyloxml
import tempfile
infile1 = sys.argv[1]
infile2 = sys.argv[2]
xmlFile = open(infile2)


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
ecceteraProject = Phyloxml()
ecceteraProject.build_from_file(speciesXML)


#Creating list of the internal node names for the ecceTERA tree
ecceteraNodes = []
for tree in ecceteraProject.get_phylogeny():
	for node in tree.traverse('postorder'):
		if node.is_leaf() == False:
			ecceteraNodes.append(node.name)
	ecceteraNodes.pop()


#Using the input chronogram to create a tree using ete3 and creating a list of the internal node names in this tree
chronoTree = Tree(infile1, format=1)
chronoNodes = []
for node in chronoTree.traverse('postorder'):
	if node.is_leaf() == False:
		chronoNodes.append(node.name)


#Setting up the created output file
outfile = open(str(infile1 + '_internal_nodes.txt'), 'w')
outfile.write('nodename	lower	upper	average' + '\n')


#Associating each node name to its early and late dates and writing in file
for i in range(len(ecceteraNodes)):
	cols = chronoNodes[i].split('_')
	earlyDate = float(cols[0])
	lateDate = float(cols[1]) #.strip()
	avgDate = (earlyDate + lateDate) / 2
	outfile.write(str(ecceteraNodes[i]) + '\t' + str(earlyDate) + '\t' + str(lateDate) + '\t' + str(avgDate) + '\n')


#Closing files
outfile.close()
speciesXML.close()
xmlFile.close()

