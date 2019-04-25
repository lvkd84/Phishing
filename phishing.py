from scipy.io import arff
import pandas as pd
import csv
import calculate


def run_calculations(a, y, l=None):
    if l==None:
        print("Phishing 1:")
        r_difference_p1, r_ratio_p1, o_ratio_p1 = calculate.calculate_ass_effects(df1, p1_index[a], p1_index[y])
    
        print("Phishing 2:")
        r_difference_p2, r_ratio_p2, o_ratio_p2 = calculate.calculate_ass_effects(df2, p2_index[a], p2_index[y])

        return [a,y,"", r_difference_p1, r_difference_p2, r_ratio_p1, r_ratio_p2, o_ratio_p1, o_ratio_p2]
        
    else:
        print("Phishing 1:")
        r_difference_p1, r_ratio_p1, o_ratio_p1 = calculate.calculate_ass_effects(df1, p1_index[a], p1_index[y], p1_index[l])
    
        print("Phishing 2:")
        r_difference_p2, r_ratio_p2, o_ratio_p2 = calculate.calculate_ass_effects(df2, p2_index[a], p2_index[y], p2_index[l])

        return [a,y,l, r_difference_p1, r_difference_p2, r_ratio_p1, r_ratio_p2, o_ratio_p1, o_ratio_p2]

if __name__== '__main__':

    '''
    For some of the attributes, we have 1=legit, 0=suspicious, and -1=phishy. To simplify, we binarize these variables putting 
    the suspicious websites in with the phishy ones setting the labels to 1=legit and 0=phishy.
    '''
    load_data1 = arff.loadarff('Phishing1.arff')
    df1 = pd.DataFrame(load_data1[0]).astype(int)
    df1=(df1.replace(-1,0)).values # move -1 (phishy) to 0 (suspicious), 0 is now phishy

    load_data2 = arff.loadarff('Phishing2.arff')
    df2 = pd.DataFrame(load_data2[0]).astype(int)
    df2=(df2.replace(-1,0)).values


    p1_index={"S":0, "W":1, "F":2, "R":3, "A":4, "T":5, "L":6, "D":7, "I":8, "P":9}
    p2_index = {"I":0, "L":1, "F":7, "R":12, "A":13, "S":15, "W":21, "D":23, "T":25, "P":30}


    results = [["A", "Y", "L", "r_difference_p1", "r_difference_p2", "r_ratio_p1", "r_ratio_p2", "o_ratio_p1", "o_ratio_p2"]]

    print("Phishing -> SSL_final_state")
    results.append(run_calculations("P", "F"))

    print("\nPhishing -> having_IP_address")
    results.append(run_calculations("P", "I"))

    print("\nPhishing -> URL_length")
    results.append(run_calculations("P", "L"))

    print("\nPhishing -> SFH")
    results.append(run_calculations("P", "S"))

    print("\nPhishing -> URL_of_anchor")
    results.append(run_calculations("P", "A"))

    print("\nPhishing -> Pop_up_window")
    results.append(run_calculations("P", "W"))

    print("\nPhishing -> Request_URL")
    results.append(run_calculations("P", "R"))

    print("\nPhishing -> Age_of_domain")
    results.append(run_calculations("P", "D"))

    print("\nPhishing -> Web_traffic")
    results.append(run_calculations("P", "T"))

    print("\nPhishing -> SSL_final_state")
    results.append(run_calculations("P", "F"))

    print("\nhaving_IP_address -> URL_length, conditioning on Phishing")
    results.append(run_calculations("I", "L", "P"))

    print("\nPop_up_window -> URL_of_anchor, conditioning on Phishing")
    results.append(run_calculations("W", "A", "P"))

    print("\nURL_of_anchor -> Pop_up_window, conditioning on Phishing")
    results.append(run_calculations("A", "W", "P"))

    print("\nPop_up_window -> Request_URL, conditioning on Phishing")
    results.append(run_calculations("W", "R", "P"))

    print("\nRequest_URL -> Pop_up_window, conditioning on Phishing")
    results.append(run_calculations("R", "W", "P"))

    print("\nSFH -> URL_of_anchor, conditioning on Phishing")
    results.append(run_calculations("S", "A", "P"))

    print("\nURL_of_anchor -> SFH, conditioning on Phishing")
    results.append(run_calculations("A", "S", "P"))

    print("\nSFH -> Request_URL, conditioning on Phishing")
    results.append(run_calculations("S", "R", "P"))

    print("\nRequest_URL -> SFH, conditioning on Phishing")
    results.append(run_calculations("R", "S", "P"))

    print("\nAge_of_domain -> Web_traffic, conditioning on Phishing")
    results.append(run_calculations("D", "T", "P"))


    myFile = open('results.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(results)