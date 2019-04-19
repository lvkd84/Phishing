#import pandas as pd
import numpy as np
import itertools

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
    # TODO: make sure this works when there are no l to sum over
    probability = 0
    for l in range(len(lcounts)):
        alSum = 0
        for y in aycounts[aValueIndex]:
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
        yValues = [1]
    if (len(aycounts)==0):
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, lValues, indexOfL)
    return cond_prob(1, 0, aycounts, lcounts) - cond_prob(0, 0, aycounts, lcounts)


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
        yValues = [1]
    if (len(aycounts)==0):
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, lValues, indexOfL)
    return cond_prob(1, 0, aycounts, lcounts) / cond_prob(0, 0, aycounts, lcounts)

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
        aValues = [0, 1] # count in the array when A = value and Y = 1
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
    return lcounts, aycounts

def count(data, indexOfA, indexOfY, aValues, yValues, lValues=[], indexOfL=[]):
    '''
    Counts a combination of all L for when a = aValues and y = yValues. 
    Values of A, Y, and L must be discrete. A and Y can be nonbinary, though L's must be binary.

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
        the values of Y to count for
        
    lValues : int array
        the values of L to count for

    lValues : int array
        the values of L to count for


    Returns
    -------
    int array
        the counts over the combinations of L for when A=aValues and Y=yValues
    int array
        the counts over the combinations of L
    '''
    assert(len(indexOfL <= 3))

    lcounts = []
    aycounts = []
    for i in range(len(data[0])): # for all elements in the data

        if len(indexOfL)==0:
            pass
        else:
            lcounts = np.zeros(np.prod(np.array(indexOfL)))
            aycounts = np.zeros_like([[lcounts for _ in yValues] for _ in aValues])
            for a in range(len(aValues)):
                for y in range(len(yValues)):
                    ayCorrect = (data[indexOfA][i] == aValues[a]) and (data[indexOfY][i] == yValues[y])
                    correctCov = True
                    lcounts_index = 0
                    if len(indexOfL)>=1:
                        for j in range(len(lValues[0])):
                            correctCov = (data[indexOfL[0]][i] == lValues[0][j])
                            lcounts_index += j
                            if len(indexOfL)>=2:
                                for k in range(len(lValues[1])):
                                    correctCov = (data[indexOfL[1]][i] == lValues[1][k]) and correctCov
                                    lcounts_index += k
                                    if len(indexOfL)==3:
                                        for q in range(len(lValues[2])):
                                            correctCov = (data[indexOfL[2]][i] == lValues[2][q]) and correctCov
                                            lcounts_index += q
                                            update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
                                    else:
                                        update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
                            else:
                                update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
                    else:
                        #should never happen
                        update_counts(ayCorrect, correctCov, aycounts, lcounts, lcounts_index, a, y)
    
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
