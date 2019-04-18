# causal/associational risk difference:
# P(Y^(a=1)=1) - P(Y^(a=0)=1) = 0
# P(Y=1|A=1) = (sum of Y=1|A=1)/(sum of A=1)
# will fancy it up later while going through notes
# needs to potentially take into account effect mods, etc.
#import pandas as pd
import numpy as np
import itertools

#load_data1 = arff.loadarff('Phishing.arff')
#df1 = pd.DataFrame(load_data[0]).astype(int)

def riskDifference(data, indexOfA, indexOfY, indexOfL=[]):
    AValues = [0, 1] # count in the array when A = value and Y = 1
    YValues = [1]
    LValues = [ [0,1] for _ in range(len(indexOfL))]
    ALCombos = [_ for l in range(len(indexOfL)+2) for _ in itertools.combinations([indexOfL,'a'], l)] 
    counts, totals = count(data, indexOfA, indexOfY, AValues, YValues, ALCombos, LValues, indexOfL)
    #return counts[1][0]/totals[1] - counts[0][0]/totals[0]

def riskRatio(data, indexOfA, indexOfY, indexOfL=[]):
    AValues = [0,1]
    YValues = [1]
    LValues = [ [0,1] for _ in range(len(indexOfL))]
    ALCombos = [_ for l in range(len(indexOfL)+2) for _ in itertools.combinations([indexOfL,'a'], l)] 
    counts, totals = count(data, indexOfA, indexOfY, AValues, YValues, ALCombos, LValues, indexOfL)
    #return (counts[1][0]/totals[1])/(counts[0][0]/totals[0])

def oddsRatio(data, indexOfA, indexOfY, indexOfL=[]):
    AValues = [0,1]
    YValues = [0,1]
    LValues = [[0,1] for _ in range(len(indexOfL))]
    ALCombos = [_ for l in range(len(indexOfL)+2) for _ in itertools.combinations([indexOfL,'a'], l)] 
    counts, totals = count(data, indexOfA, indexOfY, AValues, YValues, ALCombos, LValues, indexOfL)
    #return (counts[1][1]/totals[1]/(counts[1][0]/totals[1])/(counts[0][1]/totals[0]/(counts[0][0]/totals[0])))

def count(data, indexOfA, indexOfY, AValues, YValues, ALCombos, LValues=[], indexOfL=[]):
    #TODO: give counts and totals more descriptive names
    totals = np.zeros_like(ALCombos)
    ycounts = np.zeros_like([ALCombos for _ in range(len(YValues))])
    for i in range(len(data[0])):
        for j in range(len(ALCombos)):
            correctCov = True
            for l in indexOfL:
                if l in ALCombos[j]:
                    correctCov = data[l][i] == 1
                else:
                    correctCov = data[l][i] == 0
            if 'a' in ALCombos[j]:
                correctCov = data[indexOfA][i] == 1
            else:
                correctCov = data[indexOfA][i] == 0
            for k in YValues:
                yCorrect = data[indexOfY][i] == k
                if correctCov:
                    totals[j] += 1
                    if yCorrect:
                        ycounts[k][j] += 1
    return ycounts, totals

if __name__ == '__main__':
    data = np.array([[0,0,0,0,1,1,1], [0,1,1,1,0,1,1]])
    #A=0, Y=0 = 1
    #A=0, Y=1 = 3
    #A=1, Y=0 = 1
    #A=1, Y=1 = 2
    counts, totals = count(data, 0, 1, [0, 1], [0,1])
    print("counts: A=0|Y=0, A=0|Y=1")
    print("counts: A=1|Y=0, A=1|Y=1")
    print(counts)
    print("totals: A=0, A=1")
    print(totals)
    print("Y=1,A=1/A=1 - Y=1,A=0/A=0")
    print(riskDifference(data, 0, 1))
    print("a=1,y=1/a=1")
    print("-----------")
    print("a=0,y=1/a=0")
    print(riskRatio(data, 0, 1))
    print("a1,y1/a1 / a1,y0/a1")
    print("-------------------")
    print("a0,y1/a0 / a0,y0/a0")
    print(oddsRatio(data, 0, 1))

