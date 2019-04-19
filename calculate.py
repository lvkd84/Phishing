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


def condProb(aValueIndex, yValueIndex, aycounts, ltotals):
    '''
    Calculates the P(Y=y|A=a) when P(Y=y|A=a, L_i=l_i, ..., L_n=l_n)

    Parameters
    ----------
    P(Y=y|A=a) = \sum_L P(Y=y|A=a, L=l, ..., L=l)*P(L=l, ..., L=l)
            = \sum_L P(Y=y,A=a,L=l,...,L=l)*P(L=l,...,L=l)/P(A=a,L=l,...,L=l)
                        aycounts[a][y][i]      totals[i]      aycounts[a][sum over y][i]
    aValueIndex : int
        the index of aycounts where a = value you're looking for
    yValueIndex : int
        the index of aycounts[a] where y = value you're looking for
    aycounts : int array
        it's complicated but each value [a][y][i] is where you're on the ith combo of L
        and it's the sum of where [a][y] are their values
    ltotals : int array
        same as aycounts but no a and y
    
    Returns
    -------
    float
        P(Y=y|A=a)
    '''
    # TODO: make sure this works when there are no l to sum over
    probability = 0
    for l in range(len(ltotals)):
        alSum = 0
        for y in aycounts[aValueIndex]:
            alSum += aycounts[aValueIndex][y][l]
        probability += aycounts[aValueIndex][yValueIndex][l] * ltotals[i] / alSum
    return probability


def riskDifference(data, indexOfA, indexOfY, indexOfL=[]):
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
    
    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    Returns
    -------
    float
        the risk difference for A on Y given conditions L
    '''
    AValues = [0, 1] # count in the array when A = value and Y = 1
    YValues = [1]
    LCombos = [_ for l in range(len(indexOfL)+1) for _ in itertools.combinations([indexOfL], l)] 
    counts, totals = count(data, indexOfA, indexOfY, AValues, YValues, LCombos, indexOfL)
    return condProb(1, 0, counts, totals) - condProb(0, 0, counts, totals)


def riskRatio(data, indexOfA, indexOfY, indexOfL=[]):
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

    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    Returns
    -------
    float
        the risk ratio for A on Y given conditions L
    '''
    AValues = [0,1]
    YValues = [1]
    LCombos = [_ for l in range(len(indexOfL)+1) for _ in itertools.combinations([indexOfL], l)] 
    counts, totals = count(data, indexOfA, indexOfY, AValues, YValues, LCombos, indexOfL)
    return condProb(1, 0, counts, totals) / condProb(0, 0, counts, totals)

def oddsRatio(data, indexOfA, indexOfY, indexOfL=[]):
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

    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    Returns
    -------
    float
        the odds ratio for A on Y given conditions L
    '''
    AValues = [0,1]
    YValues = [0,1]
    LCombos = [_ for l in range(len(indexOfL)+1) for _ in itertools.combinations([indexOfL], l)]
    # contains all combinations of the indices of A and L's
    counts, totals = count(data, indexOfA, indexOfY, AValues, YValues, LCombos, indexOfL)
    return condProb(1, 1, counts, totals)/condProb(1, 0, counts, totals) / (condProb(0, 1, counts, totals)/condProb(0, 0, counts, totals))


def count(data, indexOfA, indexOfY, AValues, YValues, LCombos, indexOfL=[]):
    '''
    Counts a combination of all L for when a = AValues and y = YValues. 
    Values of A, Y, and L must be discrete. A and Y can be nonbinary, though L's must be binary.

    Parameters
    ----------
    data : int array
        the data to count over
    indexOfA : int
        the index of A in the data
    indexOfY : int
        the index of Y in the data
    AValues : int array
        the values of A to count for
    YValues : int array
        the values of Y to count for
    LCombos : int array
        permutations of all indices of L
    indexOfL : int
        the indices of L in the data

    Returns
    -------
    int array
        the counts over the permutations of L for when A=AValues and Y=YValues
    int array
        the counts over the permutations of L
    '''
    #TODO: give counts and totals more descriptive names
    totals = np.zeros_like(LCombos) # totals[j] holds the total number of items that only contain the items in LCombos[j]
    aycounts = np.zeros_like([[LCombos for _ in YValues] for _ in AValues]) # same but for each of Y=YValues[k]
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
            for a in range(len(AValues)):
                for y in range(len(YValues)):
                    ayCorrect = (data[indexOfA][i] == AValues[a]) and (data[indexOfY][i] == YValues[y])
                    if correctCov:
                        totals[j] += 1
                        if ayCorrect:
                            aycounts[a][y][j] += 1
    return aycounts, totals

