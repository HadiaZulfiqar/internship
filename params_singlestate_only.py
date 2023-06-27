import numpy as np
import h5py
import pandas as pd

''' 
                FileNames:
Tape_tensile_1-STAGE1_RESULT.erfh5
Spotwelds-STAGE1_RESULT.erfh5
Support_Case_16_5-STAGE3_RESULT.erfh5
Support_Case_16_5-STAGE2_RESULT.erfh5
Support_Case_16_5-STAGE1_RESULT.erfh5
HEMISPHERE-1-LAYER-CASE-STAGE1_RESULT.erfh5
Thermoforming_Organosheet-STAGE1_RESULT.erfh5
DDF_ESI-STAGE1_RESULT.erfh5
Test_4-STAGE1_RESULT.erfh5
TF_Spotwelds_1-STAGE1_RESULT.erfh5
cross_beam-STAGE1_RESULT.erfh5
Test_150_outer-STAGE1_RESULT.erfh5
Test_170_outer-STAGE1_RESULT.erfh5
Test6_allstages.erfh5
Test6_last_Stage.erfh5 
Test_8_150_all_allstages.erfh5
Test7_150_outer_allstages.erfh5
Test_8_150_all_last_Stage.erfh5
Test7_150_outer_last_Stage.erfh5

Test_170_opt-STAGE1_RESULT
Test_150_opt-STAGE1_RESULT

'''

#display groups and take input
def printandinput(inp, data):
    print("\n\nList of groups inside "+ inp+" are: ")
    for i in range(len(data)):
        print("Press "+str(i)+" for " +data[i])
    nextinp=input("Which subgroup do you want to access?\n")
    nextinp= check(nextinp, data)
    return int(nextinp)

#checking input    
def check(index, data):
    flag = False
    while flag==False:
        try:
            flag = True
            if (int(index) >len(data)) or index.isalpha() or index.isspace():
                raise ValueError 
        except ValueError:
            data= input("Number out of range! Enter again: ")
            flag = False
    return index
        
#merging csv files function        
def mergecsv(csvlist, index,fileName):
    df=[]
    for i in range(index):
        a = pd.read_csv(csvlist[i])
        df.append(a)    
    merged = pd.concat(df, axis=1)
    merged.to_csv(fileName[:-6]+".csv", index=False) 
    return merged

#for displaying the parameters the user have chosen
def displayparams(noofparams, csvnames):
    print("Chose from these parameters: ")
    for i in range(noofparams):
        print("Press ",i, " for "+ str(csvnames[i])[:-4])

#for checking either dataset is multidimensional or not    
def checkshape(data9,data,name):
    t=data.shape
    if t[-1]==1:
        return True
    elif t[-1]==3:
        return False  
   
#for accessing dataset of 'TIME' 
def parameters():
    # for subgrps inside post
    data_a = f.get('post')
    data1 = np.array(data_a)
    # for subgrps inside singlestate)
    data_c= data_a.get(data1[-1])
    data3= np.array(data_c)
    # for subgrp inside laststate
    data_d=data_c.get(data3[-1])
    data4= np.array(data_d)
    # for subgrp inside entityresults
    data_e= data_d.get(data4[-1])
    return data_e

def res(data_g,data7, data6,sg6):
    # for subgrp inside ZONE1_set1
    data_h= data_g.get(data7[-1])
    data8= np.array(data_h)
    # for dataset inside erfblock
    data_i= data_h.get(data8[-1])
    data9= np.array(data_i)
    # for dataset inside res
    data_j= data_i.get(data9[-1])
    data10= np.array(data_j)
    # checkshape(data9,data10)
    # saving data into csv file
    csvFileName= str(data6[sg6])+".csv"
    csvvv=str(data6[sg6])
    if checkshape(data9,data10, csvvv):
        bb=data10.flatten()             # .flatten() returns a copy of the array collapsed into one dimension
        hd= str(data6[sg6])
        np.savetxt(csvFileName,bb,header=str(hd))
    else:
        bb=data10[:,0]             # .flatten() returns a copy of the array collapsed into one dimension
        hd= str(data6[sg6])
        np.savetxt(csvFileName,bb,header=str(hd))

    return csvFileName


k=1
noofparams=[]
noofinputs=[]
sg555=[]
sg666=[]
newlist=[] 

for j in range(0,1):
                          #########CAN BE HERE###########
    # FileName, for eg('Tape_tensile_1-STAGE1_RESULT.erfh5')
    FileName=input("Enter the file you want to access: ")
    fileName= 'E:/HdfViewTool/erfh5 files/'+ FileName
    # destination = "C:/Users/binary computers/Downloads/Integrated Tool/"+ filename+"_"+ str(k)+"/"
    f = h5py.File(fileName, 'r')
    a = list(f.keys())
    d= list(f.values())
    print(a,"\n",d)
    print("\nFile: ",fileName)

    #no. of parameters
    if k==1:
        param= int(input("Enter the number of datasets you want to access: "))
    noofparams.append(param)

    #initializing list for csv file names
    csvnames=[]
                            
    for i in range(0, noofparams[j]):
        print("For dataset ", i+1)
        #group 1
        #for  getting csv file of "other parameters"
        DATA=parameters()
        ################for taking input one time only############
        
        # for subgrp inside MODEL
        data5= np.array(DATA)
        if k==1:
            sg5= printandinput("entityresults",data5)
            sg555.append(sg5)
        data_f= DATA.get(data5[sg555[i]])
        data6= np.array(data_f)
        if k==1:
            sg6 = printandinput(data5[sg555[i]], data6)
            sg666.append(sg6)
        # for subgrp inside sg6
        data_g= data_f.get(data6[sg666[i]])
        data7= np.array(data_g)
        name= res(data_g, data7,data6,sg666[i])
        csvnames.append(name)
    # generating a merged csv file    
    mergecsv(csvnames, noofparams[j],fileName)
    k+=1

# #close the file
f.close() 
