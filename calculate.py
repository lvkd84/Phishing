#import pandas as pd
import numpy as np

#load_data1 = arff.loadarff('Phishing.arff')
#df1 = pd.DataFrame(load_data[0]).astype(int)


def cond_prob(aValueIndex, yValueIndex, aycounts, lcounts):
    '''
    Calculates the P(Y=y|A=a) when P(Y=y|A=a, L_i=l_i, ..., L_n=l_n)

    Parameters
    ----------
    P(Y=y|A=a) = \sum_L P(Y=y|A=a, L=l, ..., L=l)*P(L=l, ..., L=l)
            = \sum_L P(Y=y,A=a,L=l,...,L=l)*P(L=l,...,L=l)/P(A=a,L=l,...,L=l)
                        aycounts[a][y][i]      lcounts[i]      aycounts[a][sum over y][i]
    if no L:
               = P(Y=y,A=a) / P(A=a)
               aycounts[a][y] aycounts[a][sum over y]
    aValueIndex : int
        the index of aycounts where a = value you're looking for
    yValueIndex : int
        the index of aycounts[a] where y = value you're looking for
    aycounts : int array
        it's complicated but each value [a][y][i] is where you're on the ith combo of L
        and it's the sum of where [a][y] are their values
    lcounts : int array
        same as aycounts but no a and y
    
    Returns
    -------
    float
        P(Y=y|A=a)
    '''
    probability = 0
    if len(lcounts)==0:
        #aSum = 0
        #for y in range(len(aycounts[aValueIndex])): #sum over all possible y
        #    aSum += aycounts[aValueIndex][y]
        probability = aycounts[aValueIndex][yValueIndex] / np.sum(aycounts[aValueIndex])
    else:
        for l in range(len(lcounts)):
            alSum = 0
            for y in range(len(aycounts[aValueIndex])):
                alSum += aycounts[aValueIndex][y][l]
            probability += aycounts[aValueIndex][yValueIndex][l] * lcounts[l] / alSum
    return probability


def risk_difference(data, indexOfA, indexOfY, aValues = [], yValues = [], lValues=[], indexOfL=[], aycounts = [], lcounts = []):
    '''
    Calculates the associational risk difference for the cause A, the effect Y, and the conditions L

    Parameters
    ----------
    data : int array
        the data to calculate the risk difference on. Each data[i] holds all the values of a
        variable, with data[i][j] referring to element j's value for variable i.

    indexOfA : int
        the index of the cause's values in the data. data[indexOfA][j] represents element j's value of A.

    indexOfY : int
        the index of the effect's values in the data. data[indexOfY][j] represents element j's value of Y.
    
    aValues : int array
        the values to differ A over. Must hold 2 values. The difference will be for aValues[1]-aValues[0]. Optional, default is [0, 1]

    yValues : int array
        the value that Y will be calculated over. Must hold one value. Optional, default is [1]
    
    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    lValues : int array
        the values of L to count for

    aycounts : int array
        each value [a][y][i] is where you're on the ith combo of L and it's the sum of where [a][y] are their values

    lcounts : int array
        same as aycounts but no a and y

    Returns
    -------
    float
        the risk difference for A on Y given conditions L
    '''
    if len(aValues)==0:
        aValues = [0, 1] # count in the array when A = value and Y = 1
    if len(yValues)==0:
        yValues = [0, 1]
    if len(aycounts)==0:
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, lValues, indexOfL)
    return cond_prob(1, 1, aycounts, lcounts) - cond_prob(0, 1, aycounts, lcounts)


def risk_ratio(data, indexOfA, indexOfY, aValues = [], yValues = [], lValues=[], indexOfL=[], aycounts = [], lcounts = []):
    '''
    Calculates the associational risk ratio for the cause A, the effect Y, and the conditions L

    Parameters
    ----------
    data : int array
        the data to calculate the risk ratio on. Each data[i] holds all the values of a
        variable, with data[i][j] referring to element j's value for variable i.

    indexOfA : int
        the index of the cause's values in the data. data[indexOfA][j] represents element j's value of A.

    indexOfY : int
        the index of the effect's values in the data. data[indexOfY][j] represents element j's value of Y.
    
    aValues : int array
        the values to differ A over. Must hold 2 values. The difference will be for aValues[1]-aValues[0]. Optional, default is [0, 1]

    yValues : int array
        the value that Y will be calculated over. Must hold one value. Optional, default is [1]

    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    lValues : int array
        the values of L to count for

    aycounts : int array
        each value [a][y][i] is where you're on the ith combo of L and it's the sum of where [a][y] are their values

    lcounts : int array
        same as aycounts but no a and y

    Returns
    -------
    float
        the risk ratio for A on Y given conditions L
    '''
    if len(aValues)==0:
        aValues = [0, 1] # count in the array when A = value and Y = 1
    if len(yValues)==0:
        yValues = [0, 1]
    if (len(aycounts)==0):
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, lValues, indexOfL)
    return cond_prob(1, 1, aycounts, lcounts) / cond_prob(0, 1, aycounts, lcounts)

def odds_ratio(data, indexOfA, indexOfY, aValues = [], yValues = [], lValues=[], indexOfL=[], aycounts = [], lcounts = []):
    '''
    Calculates the associational odds ratio for the cause A, the effect Y, and the conditions L

    Parameters
    ----------
    data : int array
        the data to calculate the odds ratio on. Each data[i] holds all the values of a
        variable, with data[i][j] referring to element j's value for variable i.

    indexOfA : int
        the index of the cause's values in the data. data[indexOfA][j] represents element j's value of A.

    indexOfY : int
        the index of the effect's values in the data. data[indexOfY][j] represents element j's value of Y.
    
    aValues : int array
        the values to differ A over. Must hold 2 values. The difference will be for aValues[1]-aValues[0]. Optional, default is [0, 1]

    yValues : int array
        the value that Y will be calculated over. Must hold one value. Optional, default is [1]

    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.
    
    lValues : int array
        the values of L to count for

    aycounts : int array
        each value [a][y][i] is where you're on the ith combo of L and it's the sum of where [a][y] are their values

    lcounts : int array
        same as aycounts but no a and y

    Returns
    -------
    float
        the odds ratio for A on Y given conditions L
    '''
    if len(aValues)==0:
        aValues = [0, 1]
    if len(yValues)==0:
        yValues = [0, 1]
    if (len(aycounts)==0):
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, lValues, indexOfL)
    return cond_prob(1, 1, aycounts, lcounts)/cond_prob(1, 0, aycounts, lcounts) / (cond_prob(0, 1, aycounts, lcounts)/cond_prob(0, 0, aycounts, lcounts))


def update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y):
    if correctCov:
        lcounts[lcounts_index] += 1
        if ayCorrect:
            aycounts[a][y][lcounts_index] += 1
    return aycounts, lcounts

def count(data, indexOfA, indexOfY, aValues, yValues, lValues=[], indexOfL=[]):
    '''
    Counts a combination of all L for when a = aValues and y = yValues. 

    Parameters
    ----------
    data : int array
        the data to count over

    indexOfA : int
        the index of A in the data

    indexOfY : int
        the index of Y in the data

    aValues : int array
        the values of A to count for

    yValues : int array
        the values of Y--must be every discrete value that Y can hold or math will turn out wrong
        
    lValues : int array
        the values of L to count for

    indexOfL : int array
        the indices of L to condition on in the data

    Returns
    -------
    int array
        the counts over the combinations of L for when A=aValues and Y=yValues
    int array
        the counts over the combinations of L
    '''
    assert(len(indexOfL) <= 3)

    lcounts = []
    aycounts = []
    if len(indexOfL)==0:
        aycounts = np.zeros((len(aValues), len(yValues)))
    else:
        total_lValues = []
        for values in lValues:
            total_lValues.append(len(values))
        lcounts = np.zeros(np.prod(np.array(total_lValues)))
        aycounts = np.zeros_like([[lcounts for _ in yValues] for _ in aValues])
    for i in range(len(data[0])): # for all elements in the data
        if len(indexOfL)==0:
            for a in range(len(aValues)):
                for y in range(len(yValues)):
                    if ((data[indexOfA][i] == aValues[a]) and (data[indexOfY][i] == yValues[y])):
                        aycounts[a][y] += 1
        else:
            for a in range(len(aValues)):
                for y in range(len(yValues)):
                    ayCorrect = (data[indexOfA][i] == aValues[a]) and (data[indexOfY][i] == yValues[y])
                    correctCov = True
                    lcounts_index = 0
                    if len(indexOfL)>=1:
                        for j in range(len(lValues[0])):
                            correctCov = (data[indexOfL[0]][i] == lValues[0][j]) and correctCov
                            lcounts_index += j
                            if len(indexOfL)>=2:
                                for k in range(len(lValues[1])):
                                    correctCov = (data[indexOfL[1]][i] == lValues[1][k]) and correctCov
                                    lcounts_index += k
                                    if len(indexOfL)==3:
                                        for q in range(len(lValues[2])):
                                            correctCov = (data[indexOfL[2]][i] == lValues[2][q]) and correctCov
                                            lcounts_index += q
                                            aycounts, lcounts = update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
                                    else:
                                        aycounts, lcounts = update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
                            else:
                                aycounts, lcounts = update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
                    else:
                        #should never happen
                        aycounts, lcounts = update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
    return aycounts, lcounts

def calculate_ass_effects(data, indexOfA, indexOfY, aValues = [], yValues = [], lValues=[], indexOfL=[]):
    '''
    Words

    Parameters
    ----------
    data : int array
        the data to count over

    indexOfA : int
        the index of A in the data

    indexOfY : int
        the index of Y in the data

    aValues : int array
        the values of A to count for (must have 2 items)

    yValues : int array
        the values of Y to count for (must have 2 items)
        
    indexOfL : int
        the indices of L in the data
    '''
    if len(aValues)==0:
        aValues = [0,1]
    if len(yValues)==0:
        yValues = [0,1]
    aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, lValues, indexOfL)
    
    r_difference = risk_difference(data, indexOfA, indexOfY, aValues, [yValues[1]], indexOfL, aycounts, lcounts)
    r_ratio = risk_ratio(data, indexOfA, indexOfY, aValues, [yValues[1]], indexOfL, aycounts, lcounts)
    o_ratio = odds_ratio(data, indexOfA, indexOfY, aValues, yValues, indexOfL, aycounts, lcounts)
    print("Risk difference:", r_difference)
    print("Risk ratio:", r_ratio)
    print("Odds ratio:", o_ratio)

if __name__== '__main__':
    test_data = [[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,], [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1]]
    #A=0, Y=0 = 1
    #A=0, Y=1 = 3
    #A=1, Y=0 = 1
    #A=1, Y=1 = 2
    aycounts, lcounts = count(test_data, 0, 1, [0, 1], [0,1], [[0,1]], [2])
    print("counts: A=0|Y=0, A=0|Y=1")
    print("counts: A=1|Y=0, A=1|Y=1")
    print(aycounts)
    print("totals: L (empty)")
    print(lcounts)
    print("Y=1,A=1/A=1 - Y=1,A=0/A=0")
    '''print(risk_difference(test_data, 0, 1, [0,1], []))
    print("a=1,y=1/a=1")
    print("-----------")
    print("a=0,y=1/a=0")
    print(risk_ratio(test_data, 0, 1))
    print("a1,y1/a1 / a1,y0/a1")
    print("-------------------")
    print("a0,y1/a0 / a0,y0/a0")
    print(odds_ratio(test_data, 0, 1))'''

