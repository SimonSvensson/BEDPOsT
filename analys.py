import math

#a, b:		lists
#mOffset:	     specifices maximum offset for the search 
#Returns the offset for b that results in the smallest average difference
def bestFit(a, b, mOffset):

     listfits = []

     for offset in range(-mOffset,mOffset):
	
          #Total difference
          totalDiff = 0
          #Number of times elements from both lists have been compared
          matches = 0
          for i, aValue in enumerate(a):

               bIndex = i-offset
               if (bIndex > 0 and bIndex < len(b)):
                    diff = abs(a[i]-b[bIndex])
                    totalDiff+=diff
                    matches+=1
                    
          #Average difference
          averageDiff = totalDiff/matches;
          listfits.append(averageDiff)
	
     bestOffset = -mOffset + listfits.index(min(listfits))

     return bestOffset;
 
#smoothValue:       specifices between 0 and 1 how much the graph
#                   should be smooth out, where higher means smoother
#Returns normalized dataset  
def extractFeatures(dataSet, smoothValue):

     #Smooths dataSet proportional to smoothValue
     smoothData = dataSet[:]
     chunkSize = math.floor(1/smoothValue)
     index = 0;
     while (index < len(smoothData)):
          
          rangeStart = index
          rangeStop = index + chunkSize
          averageVal = sum(smoothData[rangeStart:rangeStop + 1])/chunkSize
          for x in range(chunkSize):
               if (index+x < len(smoothData)):
                    smoothData[index+x] = averageVal
          index+=chunkSize
          
     #features will contain (original data) - (smooth out data), peaks     
     features = []
     for i, value in enumerate(dataSet):
          features.append(dataSet[i]-smoothData[i])
          
     for x in features:
          print(x)
          
     return features
	
#Main code

#bestFit should return -1
#a = [45, 37, 980, 66.2, 300, 333, 1, 1234.5, 102]
#b = [10, 66.25, 333, 333, 123, 1234.5]
#print(bestFit(a, b, 3))

#dataSet contains sin-function with random pattern on top on it, extractFeatures should extract the pattern
#dataSet =[0.2946769103,-0.1663423682,0.3553481248,0.6862579061,0.6863878879,1.056765806,0.823113492,0.893228397,0.3737555539,0.9704607905,0.8169731067,1.005231475,1.017492821,0.5487237896,0.8974913703,1.409996634,1.456861624,0.849586281,0.9702453615,1.361620437,0.829864356,0.5212090771,1.112655266,0.6124071649,0.6305480554,0.8373180984,0.4670883715,0.1211448841,-0.05422068959,0.4190553049,-0.36007804,0.06207973278,-0.4145944272,-0.1199898124,-0.1474979572,-0.5458573821,-0.7334576747,-1.007949366,-0.5726875905,-0.3936211068,-0.5093620394,-0.388505601,-0.9389020336,-0.7670342263,-0.7390952612,-1.471899157,-1.263873642,-1.470356656,-0.6723538064,-1.396693625,-0.9487820928,-1.277164113,-0.7800298045,-0.9509025279,-0.784339372,-0.3967529922,-0.07559114695,-0.5350239932,-0.05827801942,-0.6626525688,-0.2958531025,0.2977054717,-0.00473801153,0.4130317988,0.2169897823,0.717032387,0.2190410491,0.9198986571,0.7859743948,0.5104488543,0.4297914531,0.4901920107,0.4037220593,0.4913752796,0.7080536224,1.133496233,0.810309718,1.087941472,1.249202548,0.8868241903,0.7746077455,1.233840604,1.125005046,0.6717732537,0.5306810062,0.4184892844,1.017416297,1.001892372,0.173917921,0.7708871047,0.2300699248,0.216231651,-0.2940456119,0.3500416071,0.05795154748,-0.2708621935,-0.6668982117,-0.6054903721,-0.0980306899,-0.6183849255]
#extractFeatures(dataSet, 0.1);

