import sys, re
import time
from datetime import datetime


if len(sys.argv) != 3:
	print "Usage: python syncEDA_ACC.py -E=<EDA file> -A=<ACC file>"
	quit()


#find EDA file from arguments
EDAfile = ''

for x in range(1, len(sys.argv)):
	if sys.argv[x][:3] == '-E=':
		EDAfile = sys.argv[x][3:]


#find ACC file from arguments
ACCfile = ''
for x in range(1, len(sys.argv)):
	if sys.argv[x][:3] == '-A=':
		ACCfile = sys.argv[x][3:]


if len(EDAfile) < 1 or len(ACCfile) < 1:
	print "Usage: python syncEDA_ACC.py -E=<EDA file> -A=<ACC file>"
	quit()


# Get the timestamp and the samplerate from the files
EDA=open(EDAfile)
ACC=open(ACCfile)
for i in range(2):
	lineEDA=EDA.next().strip()
	lineACC=ACC.next().strip()
	if i == 0:
		timestampEDA = float(lineEDA)
		firstEntry = re.search('^[0-9\.]+', lineACC)
		timestampACC = float(firstEntry.group(0))
	else:
		samplerateEDA = float(lineEDA)
		firstEntry = re.search('^[0-9\.]+', lineACC)
		samplerateACC = float(firstEntry.group(0))
EDA.close()
ACC.close()

print "timestampEDA:", timestampEDA
print "samplerateEDA:", samplerateEDA

print "timestampACC:", timestampACC
print "samplerateACC:", samplerateACC


# determine some parameters from extracted information
offset = timestampEDA - timestampACC
print "offset (EDA-ACC):",offset

if samplerateEDA > samplerateACC:
	print "EDA has higher samplerate and should be downsampled"
	highest = "EDA"
	targetSamplerate = samplerateACC
	downFile = EDAfile
	samplesToCombine = samplerateEDA/samplerateACC
else:
	print "ACC has higher samplerate and should be downsampled"
	highest = "ACC"
	targetSamplerate = samplerateEDA
	downFile = ACCfile
	samplesToCombine =  samplerateACC/samplerateEDA

print "Samples to combine into chunks from",highest,":", samplesToCombine




# get the data from the file we are downsampling
f=open(downFile)
content = f.readlines()
f.close()
content = [x.strip() for x in content] # removes newline character and whitespace at EOL


# the data is now in 'content'
# Now downsample it
output = ''

for chunk in range(0,int((len(content)-2)/samplesToCombine)):
	piecetotal = []
	for x in range(0,int(samplesToCombine)):
		pieces = content[x+chunk*int(samplesToCombine)+2].split(",")

		for y in range(0, len(pieces)):
			if len(piecetotal) < y+1:
				piecetotal.append(0)
			piecetotal[y] += float(pieces[y])

	outRow = ''
	for x in range(0,len(piecetotal)):
		if x != 0:
			outRow += ","
		outRow += str(piecetotal[x]/samplesToCombine)
	output += outRow+"\n"

if downFile == ACCfile:
	outACC = output
	masterFile = EDAfile
else:
	outEDA = output
	masterFile = ACCfile


output = ''
# Now read the other file
f=open(masterFile)
content = f.readlines()
f.close()
content = [x.strip() for x in content] # removes newline character and whitespace at EOL

for x in range(0,len(content)-2):
	output += content[x+2]+"\n"

if masterFile == ACCfile:
	outACC = output
else:
	outEDA = output


# Great, now we need to sync them into the final outfile
finalOut = ''

if timestampEDA < timestampACC:
	finalOut += str(timestampEDA)+", "+str(timestampEDA)+", "+str(timestampEDA)+", "+str(timestampEDA)
else:
	finalOut += str(timestampACC)+", "+str(timestampACC)+", "+str(timestampACC)+", "+str(timestampACC)

finalOut += "\n"+str(targetSamplerate)+", "+str(targetSamplerate)+", "+str(targetSamplerate)+", "+str(targetSamplerate)



# How much do they differ in time, and how many entries should we shift them?
shift = offset*targetSamplerate


#lines are better... make it lines instead of massive strings
linesEDA = outEDA.split("\n")
linesACC = outACC.split("\n")

EDAcounter = 0
ACCcounter = 0
if shift < 0:
	while shift < 0:
		finalOut += "\n"+linesEDA[EDAcounter]+",,,"
		shift += 1
		EDAcounter += 1
else:
	while shift > 0:
		finalOut += "\n,"+linesACC[ACCcounter]
		shift -= 1
		ACCcounter += 1

#print finalOut

# Now, just print the rest
counter = 0
while len(linesEDA) > counter+EDAcounter or len(linesACC) > counter+ACCcounter:
	finalOut += "\n"+(linesEDA[counter+EDAcounter] if len(linesEDA) > counter+EDAcounter and len(linesEDA[counter+EDAcounter]) > 0 else "")+","+(linesACC[counter+ACCcounter] if len(linesACC) > counter+ACCcounter and len(linesACC[counter+ACCcounter]) > 0 else ",,")
	counter += 1





print finalOut

