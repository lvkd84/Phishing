#import pandas as pd
import numpy as np

#load_data1 = arff.loadarff('Phishing.arff')
#df1 = pd.DataFrame(load_data[0]).astype(int)


def cond_prob(aValueIndex, yValueIndex, aylcounts):
    '''
    Calculates the P(Y=y|A=a) when P(Y=y|A=a, L_i=l_i, ..., L_n=l_n)

    Parameters
    ----------
    P(Y=y|A=a) = \sum_L P(Y=y|A=a, L=l, ..., L=l)*P(L=l, ..., L=l)
            = \sum_L P(Y=y,A=a,L=l,...,L=l)*P(L=l,...,L=l)/P(A=a,L=l,...,L=l)
                        aylcounts[a][y][i]      lcounts[i]      aylcounts[a][sum over y][i]
    if no L:
               = P(Y=y,A=a) / P(A=a)
               aylcounts[a][y] aylcounts[a][sum over y]
    aValueIndex : int
        the index of aylcounts where a = value you're looking for
    yValueIndex : int
        the index of aylcounts[a] where y = value you're looking for
    aylcounts : int array
        it's complicated but each value [a][y][i] is where you're on the ith combo of L
        and it's the sum of where [a][y] are their values
    lcounts : int array
        same as aylcounts but no a and y
    
    Returns
    -------
    float
        P(Y=y|A=a)
    '''
    probability = 0
    if np.shape(aylcounts)==(2,2):
        probability = aylcounts[aValueIndex][yValueIndex] / np.sum(aylcounts[aValueIndex])
    else:
        for l in range(len(aylcounts[aValueIndex][yValueIndex])):
            alSum = 0
            lsum = 0
            for y in range(len(aylcounts[aValueIndex])):
                alSum += aylcounts[aValueIndex][y][l]
                for a in range(2):
                    lsum += aylcounts[a][y][l]
            probability += aylcounts[aValueIndex][yValueIndex][l] * lsum / alSum
    if (probability==0):
        raise ValueError("Positivity was violated when calculating P(Y="+str(yValueIndex)+"|A="+str(aValueIndex)")")
    return probability


def risk_difference(data, indexOfA, indexOfY, aylcounts = [], indexOfL=None):
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

    aylcounts : int array
        each value [a][y][i] is where you're on the ith combo of L and it's the sum of where [a][y] are their values

    lcounts : int array
        same as aylcounts but no a and y

    Returns
    -------
    float
        the risk difference for A on Y given conditions L
    '''
    if len(aylcounts)==0:
        aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    return cond_prob(1, 1, aylcounts) - cond_prob(0, 1, aylcounts)


def risk_ratio(data, indexOfA, indexOfY, aylcounts = [], indexOfL = None):
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

    aylcounts : int array
        each value [a][y][i] is where you're on the ith combo of L and it's the sum of where [a][y] are their values

    lcounts : int array
        same as aylcounts but no a and y

    Returns
    -------
    float
        the risk ratio for A on Y given conditions L
    '''
    if (len(aylcounts)==0):
        aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    return cond_prob(1, 1, aylcounts) / cond_prob(0, 1, aylcounts)

def odds_ratio(data, indexOfA, indexOfY, aylcounts = [], indexOfL=None):
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

    aylcounts : int array
        each value [a][y][i] is where you're on the ith combo of L and it's the sum of where [a][y] are their values

    lcounts : int array
        same as aylcounts but no a and y

    Returns
    -------
    float
        the odds ratio for A on Y given conditions L
    '''
    if (len(aylcounts)==0):
        aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    return cond_prob(1, 1, aylcounts)/cond_prob(1, 0, aylcounts) / (cond_prob(0, 1, aylcounts)/cond_prob(0, 0, aylcounts))


def count(data, indexOfA, indexOfY, indexOfL=None):
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
    values = [0, 1]
    aylcounts = []
    if indexOfL==None:
        aylcounts = np.zeros((len(values), len(values)))
    else:
        aylcounts = np.zeros((len(values), len(values), len(values)))
    for i in range(len(data[0])): # for all elements in the data
        if indexOfL==None:
            for a in range(len(values)):
                for y in range(len(values)):
                    if ((data[indexOfA][i] == values[a]) and (data[indexOfY][i] == values[y])):
                        aylcounts[a][y] += 1
        else:
            for a in range(len(values)):
                for y in range(len(values)):
                    for l in range(len(values)):
                        if ((data[indexOfA][i] == values[a]) and (data[indexOfY][i] == values[y]) and (data[indexOfL][i] == values[l])):
                            aylcounts[a][y][l] += 1
    return aylcounts

def calculate_ass_effects(data, indexOfA, indexOfY, indexOfL=None):
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
    aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    
    r_difference = risk_difference(data, indexOfA, indexOfY, aylcounts, indexOfL)
    r_ratio = risk_ratio(data, indexOfA, indexOfY, aylcounts, indexOfL)
    o_ratio = odds_ratio(data, indexOfA, indexOfY, aylcounts, indexOfL)
    print("Risk difference:", r_difference)
    print("Risk ratio:", r_ratio)
    print("Odds ratio:", o_ratio)
    return r_difference, r_ratio, o_ratio

if __name__== '__main__':
    test_data = [[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,], [0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,1,1,1,1,1]]
    #A=0, Y=0 = 1
    #A=0, Y=1 = 3
    #A=1, Y=0 = 1
    #A=1, Y=1 = 2
    aycounts = count(test_data, 0, 1)
    print("counts: A=0|Y=0, A=0|Y=1")
    print("counts: A=1|Y=0, A=1|Y=1")
    print(aycounts)
    print("Y=1,A=1/A=1 - Y=1,A=0/A=0")
    print(calculate_ass_effects(test_data, 0, 1))
    aylcounts = count(test_data, 0, 1, 2)
    print("A0Y0L0, A0Y0L1")
    print("A0Y1L0, A0Y1L1")
    print("A1Y0L0, A1Y0L1")
    print("A1Y1L0, A1Y1L1")
    print(aylcounts)
    print("put l in")
    print(calculate_ass_effects(test_data, 0, 1, 2))

