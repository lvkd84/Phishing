# causal/associational risk difference:
# P(Y^(a=1)=1) - P(Y^(a=0)=1) = 0
# P(Y=1|A=1) = (sum of Y=1|A=1)/(sum of A=1)
# will fancy it up later while going through notes
# needs to potentially take into account effect mods, etc.
#import pandas as pd
import numpy as np

#load_data1 = arff.loadarff('Phishing.arff')
#df1 = pd.DataFrame(load_data[0]).astype(int)

def riskDifference(data, indexOfA, indexOfY):
    countWhenA = [0, 1] # count in the array when A = value and Y = 1
    countWhenY = [1]
    counts, totals = count(data, indexOfA, indexOfY, countWhenA, countWhenY)
    return counts[1][0]/totals[1] - counts[0][0]/totals[0]

def riskRatio(data, indexOfA, indexOfY):
    countWhenA = [0,1]
    countWhenY = [1]
    counts, totals = count(data, indexOfA, indexOfY, countWhenA, countWhenY)
    return (counts[1][0]/totals[1])/(counts[0][0]/totals[0])

def oddsRatio(data, indexOfA, indexOfY):
    countWhenA = [0,1]
    countWhenY = [0,1]
    counts, totals = count(data, indexOfA, indexOfY, countWhenA, countWhenY)
    return (counts[1][1]/totals[1]/(counts[1][0]/totals[1])/(counts[0][1]/totals[0]/(counts[0][0]/totals[0])))

def count(data, indexOfA, indexOfY, countWhenA, countWhenY):
    counts = np.zeros((len(countWhenA), len(countWhenY)))
    totals = np.zeros(len(countWhenA))
    for i in range(len(data[0])):
        for j in range(len(countWhenA)):
            if (data[indexOfA][i] == countWhenA[j]):
                totals[j] += 1
                for k in range(len(countWhenY)):
                    if (data[indexOfY][i] == countWhenY[k]):
                        counts[j][k] += 1
    return counts, totals

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

