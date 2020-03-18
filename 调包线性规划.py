#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import re
import copy
import sys
from scipy import optimize


# In[2]:


f=open("input.txt", "r", encoding="utf-8")
str_f=f.read()
f.close()


# In[3]:


list_origin=[]
list_origin=str_f.split("\n")


# In[4]:


def confirm():
    xmax=1
    for i in list_origin:
        while(1):
            if "x"+str(xmax) in i:
                xmax+=1
            else: break
    return xmax-1
xmax=xused=confirm()


# In[5]:


free=[]
positive=[]
negtive=[]
for i in range(1,xused+1):
    if "x"+str(i)+">=0" in list_origin:
        positive.append(i)
    elif "x"+str(i)+"<=0" in list_origin:
        negtive.append(i)
    else:
        free.append(i)


# In[6]:


for a in range(1,xused+1):
    for i in list_origin:
        if i == "x"+str(a)+">=0":
            list_origin.remove(i)


# In[7]:


global addxi
addxi=xused
def Normalization(i):
    global addxi
    if "<=" in i:
        addxi+=1
        return i.replace("<=","+x"+str(addxi)+"=")
    elif ">=" in i:
        addxi+=1
        return i.replace(">=","-x"+str(addxi)+"=")
    return i
list_normal=list(map(Normalization,list_origin))
k=0
for i in list_normal:
    for j in range(1,addxi+1):
        i=list_normal[k]
        if ("*x"+str(j)) not in i:
            list_normal[k]=i.replace("x"+str(j),"1*x"+str(j))
    k+=1
fn=[[]]
p=0
for i in list_normal:
    num=0
    flag1=0
    flag2=0
    for j in i:
        if j in ["0","1","2","3","4","5","6","7","8","9"]:
            num=num+1
        if j is "-":
            if flag1==0:
                fn.append([])
                flag2=1
                flag=1
            fn[p].append(num)
    if flag2==0:
        fn.append([])
    p=p+1
fn


# In[8]:


TEMP=[]

A=[]
for i in range(len(list_normal)-1):
    A.append([])
    for j in range(addxi):
        A[i].append(0)

B=[]
for i in range(len(list_normal)):
    B.append([0])

C=[0 for i in range(0,len(list_normal))]

for i in list_normal:
    temp=re.findall(r"\d+\.?\d*",i)
    TEMP.append(temp)
TEMP=list(map(lambda x:list(map(int, x)), TEMP))

for i in range(0,len(TEMP)):
    if fn != [[]]:
        for j in range(0,len(fn[i])):
            TEMP[i][fn[i][j]]=TEMP[i][fn[i][j]]*-1
    
for i in range(1,len(TEMP)):
    for j in range(0,len(TEMP[i])-1,2):
        A[i-1][TEMP[i][j+1]-1]=TEMP[i][j]

for i in range(1,len(list_normal)):
    B[i][0]=TEMP[i][-1]

C=TEMP[0][::2]
C += [0 for i in range(len(C),addxi)]
if "min" in list_origin[0]:
    CNEW=[-l for l in C]
else:
    CNEW=copy.deepcopy(C)
flag=1


# In[9]:


if flag:
    del B[0]
    flag=0

z = np.array(CNEW)
a = np.array(A)
b = np.array(B).T

bounds_list=[]
for i in range(len(CNEW)):
    if i in free:
        bounds_list.append((None, None))
    elif i in free:
        bounds_list.append((None, 0))
    else:
        bounds_list.append((0, None))

bounds_tuple=tuple(bounds_list)

res = optimize.linprog(-z, A_eq=a, b_eq=b,bounds=(bounds_tuple))
if "max" in list_origin[0]:
    res.fun = - res.fun
print(res)
n=len(CNEW)-xused
res.x=res.x[:-n]


# In[10]:


f=open("output.txt", "w", encoding="utf-8")
f.truncate()
f.write(str(res))
f.close()


# In[ ]:




