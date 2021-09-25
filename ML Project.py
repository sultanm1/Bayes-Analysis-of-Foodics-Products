#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Installing Libraries and Such

import sys
assert sys.version_info >= (3, 5) # python>=3.5
import sklearn
assert sklearn.__version__ >= "0.20" # sklearn >= 0.20

import numpy as np #numerical package in python
import os
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt #plotting package

# to make this notebook's output identical at every run
np.random.seed(42)


# In[3]:


#Importing Pandas and my data (order items)

import pandas as pd

data = pd.read_csv("OrderItems.csv")

data


# In[4]:


data.shape


# OK
# 
# Now we would have to organize the data, we need to have the data in this format
# 
# ((order_ref, product, product, product ....)
#  (order_ref, product, product)
#  (order_ref, product, product) ...)
# 
# 
# So now let's organize by type
# 
# 

# In[5]:


data.head()


# In[6]:


new = data.loc[(data['type'] == 'Product') & (data['status'] == 'Done')]
dataNames = new[['sku', 'name']]
new = new[['order_reference', 'sku']] 


dataNames


# In[7]:


df = new.copy()
df.values


# In[8]:


#Bayes Algorithm

#Create a table of dependencies:
    #P(B | A) = Probability of B given A
    # P(B | A) = P(A&B)/P(A)
    #So, all that we need to find out is the easiest way to make the table 
    #of P(A&B)


# In[9]:


new.groupby(['order_reference'])
new


# 

# In[ ]:





# In[10]:


gro = new
gro.reset_index(drop = True, inplace = True)

gro = gro.groupby(['order_reference'])
print(type(gro))

# new.groups
# new.first()
gro.get_group(1)

#OK! So what this is saying is that order reference 1, has the three sku's 2,5, and 9


# In[11]:


#Ok, new plan is to have a 2D list
#First grab the list of names, sort and convert them into an index e.g. Specialty --> 5

#Then 12 


# In[12]:


dataNames = dataNames.drop_duplicates(subset=None, keep='first', inplace=False)
dataNames.reset_index(drop = True, inplace = True)
justSKU = dataNames["sku"]

numRows = justSKU.shape[0]
mydict = dict(justSKU)
print(mydict)

def getIndexfromValue(val):
    index = -1
    for keys,values in mydict.items():
        if mydict[keys] == val:
            return keys
    return index

getIndexfromValue("sk-0004")
    
# print(justSKU)
# numRows


# From the results above, we find out there are 17 products! 
# 
# Now we make a 17 by 17 array to calculate the 2D dependencies

# In[13]:


type(new)


# In[14]:


jointArray = np.zeros((numRows,numRows))
print(jointArray)

currentRefNum = 1
howManyAbove = 0

def addToJointArray(j, howManyAbove):
    orderArr = new.loc[j - howManyAbove:j, :]
    orderArr.reset_index(drop = True, inplace = True)
    print(orderArr)

    if orderArr.shape[0] == 1:
        #Do nothing here, because there is no relation w nothing else
        return
    for i in range(0, orderArr.shape[0]):
        for x in range(i, orderArr.shape[0]):
            firstIndex = getIndexfromValue(orderArr["sku"].loc[i])
            secondIndex = getIndexfromValue(orderArr["sku"].loc[x])
            if firstIndex != secondIndex:
                print(firstIndex, secondIndex)
                jointArray[firstIndex][secondIndex] = jointArray[firstIndex][secondIndex] + 1
                print("First index " , firstIndex, "second index" , secondIndex, "total is ", jointArray[firstIndex][secondIndex])
    return

for i in range(0, new.shape[0]):
    j = i+1
    if j == new.shape[0]:
        break
    if new["order_reference"][j] != currentRefNum:
        addToJointArray(i, howManyAbove)
        currentRefNum = new["order_reference"][j]
        howManyAbove = 0
    else:
        howManyAbove = howManyAbove + 1

# for i in range(0, jointArray.shape[0]):
#     for j in range(0, jointArray.shape[1]):
#         jointArray[i][j] = i


# In[15]:


jointArray


# In[16]:


totals = np.zeros(numRows)
for i in range(0, new.shape[0]):
    index = getIndexfromValue(new["sku"].loc[i])
    totals[index] = totals[index] + 1

print(totals)


# OK! Now we have two arrays. One is jointarrays which is the P(A&B) part of the project, which calculates how many 
# times a certain combination of 2 products was repeated. The other array is total which P(B) which just states
# the number of times the a product was repeated

# In[17]:


conditionalProb = np.zeros((numRows,numRows))

for i in range(0, numRows):
    for j in range(0, numRows):
        conditionalProb[i][j] = (jointArray[i][j] + jointArray[j][i]) / totals[i]
        
print(conditionalProb)


# So now with this arrray we get the highest probabilities from 0 to 1 of the greatest connections between items





