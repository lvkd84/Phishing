import numpy as np

def cond_prob(aValueIndex, yValueIndex, aylcounts):
    '''
    Calculates the P(Y=y|A=a) when P(Y=y|A=a, L=l) using standardization
    P(Y=y|A=a) = \sum_L P(Y=y|A=a, L=l)*P(L=l)
            = \sum_L P(Y=y,A=a,L=l)*         P(L=l)/                                                                                 P(A=a,L=l)
                    aylcounts[a][y][l]      aylcounts[sum over a][sum over y][l]/aylcounts[sum over a][sum over y][sum over l]      aylcounts[a][sum over y][l]
    if no L:
               = P(Y=y,A=a) /   P(A=a)
               aylcounts[a][y]  aylcounts[a][sum over y]

    Parameters
    ----------
    aValueIndex : int
        the index of aylcounts where a = value you're looking for (same as value of A since A is binary)
    yValueIndex : int
        the index of aylcounts[a] where y = value you're looking for (same as value of Y since Y is binary)
    aylcounts : int array
        aylcounts[a][y][l] is the number of instances where A==a, Y==y, and L==l
    
    Returns
    -------
    float
        P(Y=yValueIndex|A=aValueIndex)
    '''
    probability = 0
    if np.shape(aylcounts)==(2,2):
        probability = aylcounts[aValueIndex][yValueIndex] / np.sum(aylcounts[aValueIndex])
    else:
        for l in range(len(aylcounts[aValueIndex][yValueIndex])):
            alsum = 0
            lsum = 0
            for y in range(len(aylcounts[aValueIndex])):
                alsum += aylcounts[aValueIndex][y][l]
                for a in range(2):
                    lsum += aylcounts[a][y][l]
            total = np.sum(aylcounts)
            if (alsum == 0):
                #print("Positivity was violated when calculating P(Y="+str(yValueIndex)+"|A="+str(aValueIndex)+")")
                probability = None
                break
            else:
                probability += aylcounts[aValueIndex][yValueIndex][l] * lsum / (alsum * total)
    if (probability==0):
        #print("Positivity was violated when calculating P(Y="+str(yValueIndex)+"|A="+str(aValueIndex)+")")
        probability = None
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

    aylcounts : int array
        aylcounts[a][y][l] is the number of instances where A==a, Y==y, and L==l
    
    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    Returns
    -------
    float
        the risk difference for A on Y given conditions L
    '''
    if len(aylcounts)==0:
        aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    a1 = cond_prob(1, 1, aylcounts)
    a0 = cond_prob(0, 1, aylcounts)
    if (a1==None) or (a0==None):
        return None
    return a1 - a0


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

    aylcounts : int array
        aylcounts[a][y][l] is the number of instances where A==a, Y==y, and L==l
    
    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    Returns
    -------
    float
        the risk ratio for A on Y given conditions L
    '''
    if (len(aylcounts)==0):
        aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    a1 = cond_prob(1, 1, aylcounts)
    a0 = cond_prob(0, 1, aylcounts)
    if (a1==None) or (a0==None):
        return None
    return a1 / a0

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

    aylcounts : int array
        aylcounts[a][y][l] is the number of instances where A==a, Y==y, and L==l
    
    indexOfL : int 
        an array holding the indices of different L's values in the data. Optional.

    Returns
    -------
    float
        the odds ratio for A on Y given conditions L
    '''
    if (len(aylcounts)==0):
        aylcounts = count(data, indexOfA, indexOfY, indexOfL)
    a1y1 = cond_prob(1, 1, aylcounts)
    a0y1 = cond_prob(0, 1, aylcounts)
    a1y0 = cond_prob(1, 0, aylcounts)
    a0y0 = cond_prob(0, 0, aylcounts)
    if (a1y1==None) or (a0y1==None) or (a1y0==None) or (a0y0==None):
        return None
    return a1y1/a1y0 / (a0y1/a0y0)


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

    indexOfL : int array
        the indices of L to condition on in the data

    Returns
    -------
    int array
        aylcounts[a][y][l]: the number of instances where A==a, Y==y, and L==l
    '''
    values = [0, 1]
    aylcounts = []
    if indexOfL==None:
        aylcounts = np.zeros((len(values), len(values)))
    else:
        aylcounts = np.zeros((len(values), len(values), len(values)))
    for i in range(len(data)): # for all elements in the data
        if indexOfL==None:
            for a in range(len(values)):
                for y in range(len(values)):
                    if ((data[i][indexOfA] == values[a]) and (data[i][indexOfY] == values[y])):
                        aylcounts[a][y] += 1
        else:
            for a in range(len(values)):
                for y in range(len(values)):
                    for l in range(len(values)):
                        if ((data[i][indexOfA] == values[a]) and (data[i][indexOfY] == values[y]) and (data[i][indexOfL] == values[l])):
                            aylcounts[a][y][l] += 1
    for a in range(len(aylcounts)):
        for y in range(len(aylcounts[a])):
            if indexOfL==None:
                if aylcounts[a][y]==0:
                    print("Positivity violated for A="+str(a)+", Y="+str(y))
            else:
                for l in range(len(aylcounts[a][y])):
                    if aylcounts[a][y][l]==0:
                        print("Positivity violated for A="+str(a)+", Y="+str(y)+", L="+str(l))
    return aylcounts

def calculate_ass_effects(data, indexOfA, indexOfY, indexOfL=None):
    '''
    Calculates, prints, and returns the associational effects of A on Y given L

    Parameters
    ----------
    data : int array
        the data to count over

    indexOfA : int
        the index of A in the data

    indexOfY : int
        the index of Y in the data
        
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

