from scipy.io import arff
import pandas as pd
import csv
import calculate


def run_calculations(results, a, y, l=None):
    if l==None:
        print("Phishing 1:")
        r_difference, r_ratio, o_ratio = calculate.calculate_ass_effects(df1, p1_index[a], p1_index[y])
        results.append(["P1", a, y, "", r_difference, r_ratio, o_ratio])
    
        print("Phishing 2:")
        r_difference, r_ratio, o_ratio = calculate.calculate_ass_effects(df2, p2_index[a], p2_index[y])
        results.append(["P2", a, y, "", r_difference, r_ratio, o_ratio])
        
    else:
        print("Phishing 1:")
        r_difference, r_ratio, o_ratio = calculate.calculate_ass_effects(df1, p1_index[a], p1_index[y], p1_index[l])
        results.append(["P1", a, y, l, r_difference, r_ratio, o_ratio])
    
        print("Phishing 2:")
        r_difference, r_ratio, o_ratio = calculate.calculate_ass_effects(df2, p2_index[a], p2_index[y], p2_index[l])
        results.append(["P2", a, y, l, r_difference, r_ratio, o_ratio])
    
    return results

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


    p1_index={"S":0, "P":1, "H":2, "R":3, "A":4, "T":5, "L":6, "D":7, "I":8, "Ph":9}
    p2_index = {"I":0, "L":1, "H":7, "R":12, "A":13, "S":15, "P":21, "D":23, "T":25, "Ph":30}


    results = [["Dataset", "A", "Y", "L", "r_difference", "r_ratio", "o_ratio"]]

    print("Phishing -> SSL_final_state")
    results = run_calculations(results,"Ph", "H")

    print("\nPhishing -> having_IP_address")
    results = run_calculations(results,"Ph", "I")

    print("\nPhishing -> URL_length")
    results = run_calculations(results,"Ph", "L")

    print("\nPhishing -> SFH")
    results = run_calculations(results,"Ph", "S")

    print("\nPhishing -> URL_of_anchor")
    results = run_calculations(results,"Ph", "A")

    print("\nPhishing -> Pop_up_window")
    results = run_calculations(results,"Ph", "P")

    print("\nPhishing -> Request_URL")
    results = run_calculations(results,"Ph", "R")

    print("\nPhishing -> Age_of_domain")
    results = run_calculations(results,"Ph", "D")

    print("\nPhishing -> Web_traffic")
    results = run_calculations(results,"Ph", "T")

    print("\nPhishing -> SSL_final_state")
    results = run_calculations(results,"Ph", "H")

    print("\nhaving_IP_address -> URL_length, conditioning on Phishing")
    results = run_calculations(results,"I", "L", "Ph")

    print("\nPop_up_window -> URL_of_anchor, conditioning on Phishing")
    results = run_calculations(results,"P", "A", "Ph")

    print("\nURL_of_anchor -> Pop_up_window, conditioning on Phishing")
    results = run_calculations(results,"A", "P", "Ph")

    print("\nPop_up_window -> Request_URL, conditioning on Phishing")
    results = run_calculations(results,"P", "R", "Ph")

    print("\nRequest_URL -> Pop_up_window, conditioning on Phishing")
    results = run_calculations(results,"R", "P", "Ph")

    print("\nSFH -> URL_of_anchor, conditioning on Phishing")
    results = run_calculations(results,"S", "A", "Ph")

    print("\nURL_of_anchor -> SFH, conditioning on Phishing")
    results = run_calculations(results,"A", "S", "Ph")

    print("\nSFH -> Request_URL, conditioning on Phishing")
    results = run_calculations(results,"S", "R", "Ph")

    print("\nRequest_URL -> SFH, conditioning on Phishing")
    results = run_calculations(results,"R", "S", "Ph")

    print("\nAge_of_domain -> Web_traffic, conditioning on Phishing")
    results = run_calculations(results,"D", "T", "Ph")


    myFile = open('results.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(results)