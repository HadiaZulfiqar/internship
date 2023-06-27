import numpy as np
import pprint
import h5py
import pandas as pd

f = h5py.File('C:/Users/binary computers/Downloads/Tolook/pcfilemodification/Tape_tensile_1-STAGE1_RESULT.erfh5', 'r')
a = list(f.keys())
d= list(f.values())
print("\n\n",d)

print("list of datasets", a)
# user_inp = input("enter the dataset you want to access: ")

data_b = f.get('CSMEXPL')
data2 = np.array(data_b)
print("list of subgrps inside CSMEXPL", data2)


## for dataset inside post
# post= f[a[0]]
# b= list(post.keys())
# for subgrps inside post
# data_a = f.get('post')
# data1 = np.array(data_a)
# print("list of subgrps inside post", data1)

## for dataset inside post
post= f[a[0]]
b= list(post.keys())
# e=list(post.values())
# g= list(post.items())
# print("\n\n items in the list are: \n", g)
# print("\n\n",e)


# for subgrps inside post
data_a = f.get('post')
data1 = np.array(data_a)
print("list of subgrps inside post", data1)

# for subgrps inside subgrps of post (let's say we chose multistate)
data_c= data_a.get(data1[2])
data3= np.array(data_c)
print("\ndata3333",data3)

# for subgrp inside TIMESERIES
data_d=data_c.get(data3[0])
data4= np.array(data_d)
print("\ndata444",data4)

# for subgrp inside multientityresults
data_e= data_d.get(data4[0])
data5= np.array(data_e)
print("\ndataa555", data5)

# for subgrp inside SHELL
data_f= data_e.get(data5[4])
data6= np.array(data_f)
print("\ndataa666", data6)

# for subgrp inside Total_Stress
data_g= data_f.get(data6[-1])
data7= np.array(data_g)
print("\ndataa77", data7)


# for subgrp inside ZONE1_set1
data_h= data_g.get(data7[-1])
data8= np.array(data_h)
print("\ndataa88", data8)

# for dataset inside erfblock
data_i= data_h.get(data8[-1])
data9= np.array(data_i)
print("\ndataa99", data9)

# for dataset inside res
data_j= data_i.get(data9[-1])
data10= np.array(data_j)
t=data10.shape
print("\noriginal array have shape: ", t)
print("\n",data10)
# data10=np.array(np.arange(data_j)).reshape(2,3,4)
t=data10[:,0,0].shape
print("\narray along x axis only have shape: ",t)
print("\n",data10[:,0,0] )


#  # saving data into csv file
# csvFileName= "hello.csv"
# # csvFileName="mergedoutput.csv"
# bb=data10[:,0,0]           
# np.savetxt(csvFileName,bb,header="total stress")

    

print("\n")
f.close()
