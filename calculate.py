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
        probability += aycounts[aValueIndex][yValueIndex][l] * lcounts[i] / alSum
    return probability


def risk_difference(data, indexOfA, indexOfY, aValues = [], yValues = [], indexOfL=[], LCombos=[], aycounts = [], lcounts = []):
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

    LCombos : int array
        contains all combinations of the indices of L. Optional.

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
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, indexOfL, LCombos)
    return cond_prob(1, 0, aycounts, lcounts) - cond_prob(0, 0, aycounts, lcounts)


def risk_ratio(data, indexOfA, indexOfY, aValues = [], yValues = [], indexOfL=[], LCombos=[], aycounts = [], lcounts = []):
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

    LCombos : int array
        contains all combinations of the indices of L. Optional

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
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, indexOfL, LCombos)
    return cond_prob(1, 0, aycounts, lcounts) / cond_prob(0, 0, aycounts, lcounts)

def odds_ratio(data, indexOfA, indexOfY, aValues = [], yValues = [], indexOfL=[], LCombos=[], aycounts = [], lcounts = []):
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
    
    LCombos : int array
        contains all combinations of the indices of L. Optional.

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
        aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, indexOfL, LCombos)
    return cond_prob(1, 1, aycounts, lcounts)/cond_prob(1, 0, aycounts, lcounts) / (cond_prob(0, 1, aycounts, lcounts)/cond_prob(0, 0, aycounts, lcounts))


def count(data, indexOfA, indexOfY, aValues, yValues, indexOfL=[], LCombos=[]):
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
        
    indexOfL : int
        the indices of L in the data

    LCombos : int array
        contains all combinations of the indices of L


    Returns
    -------
    int array
        the counts over the combinations of L for when A=aValues and Y=yValues
    int array
        the counts over the combinations of L
    '''
    #TODO: give counts and lcounts more descriptive names
    if len(LCombos)==0:
        LCombos = [_ for l in range(len(indexOfL)+1) for _ in itertools.combinations([indexOfL], l)]
    lcounts = np.zeros_like(LCombos) # lcounts[j] holds the total number of items that only contain the items in LCombos[j]
    aycounts = np.zeros_like([[LCombos for _ in yValues] for _ in aValues]) # same but for each of Y=yValues[k]
    for i in range(len(data[0])): # for all elements in the data
        for j in range(len(LCombos)): # for all combos of A and L
            correctCov = True # start off with correctCov as true
            for l in indexOfL: # check that all the L's that LCombs call for are present
                if l in LCombos[j]:
                    correctCov = (data[l][i] == 1) and correctCov
                else:
                    correctCov = (data[l][i] == 0) and correctCov
                if (not(correctCov)):
                    break
            for a in range(len(aValues)):
                for y in range(len(yValues)):
                    ayCorrect = (data[indexOfA][i] == aValues[a]) and (data[indexOfY][i] == yValues[y])
                    if correctCov:
                        lcounts[j] += 1
                        if ayCorrect:
                            aycounts[a][y][j] += 1
    return aycounts, lcounts

def calculate_ass_effects(data, indexOfA, indexOfY, aValues = [], yValues = [], indexOfL=[]):
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
    LCombos = [_ for l in range(len(indexOfL)+1) for _ in itertools.combinations([indexOfL], l)]
    aycounts, lcounts = count(data, indexOfA, indexOfY, aValues, yValues, indexOfL, LCombos)
    print("Risk difference")
    r_difference = risk_difference(data, indexOfA, indexOfY, aValues, [yValues[1]], indexOfL, LCombos, aycounts, lcounts)
    print(r_difference)
    print("Risk ratio")
    r_ratio = risk_ratio(data, indexOfA, indexOfY, aValues, [yValues[1]], indexOfL, LCombos, aycounts, lcounts)
    print(r_ratio)
    print("Odds ratio")
    o_ratio = odds_ratio(data, indexOfA, indexOfY, aValues, yValues, indexOfL, LCombos, aycounts, lcounts)
