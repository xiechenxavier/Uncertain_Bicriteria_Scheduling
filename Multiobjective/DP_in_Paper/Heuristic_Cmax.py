#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 05:53:12 2022

@author: xiechen
"""
import numpy as np

with open("Gene_Experiment/Gurobi/scheduling_part/Uncertain_Bicriteria_Scheduling/Multiobjective/temp_toy.txt") as f:
    lines = f.readlines()
    M = set(map(int,lines[0].strip('\n').split(',')))
    # jobs set
    J = set(map(int,lines[1].strip('\n').split(',')))
    # scenario set
    U = set([u for u in range(0,20)])
    
    Kj = list(map(float,lines[2].strip('\n').split(','))) #
    Bj = list(map(int,lines[3].strip('\n').split(',')))
    
# Generate Ps
def Generate_Ps(J):
    Ps = {}
    for u in range(0,20):
        Ps[u] = []
        for j in J:
            Ps[u].append(Kj[j] * u + Bj[j])

    return Ps

Ps = Generate_Ps(J) # Ps is the table of processing time of all jobs in every scenario
# print(Ps)

def DP_test(n,pt1,m):
    # S0 = (0,0,0,[])
    S0 = []
    for i in range(0, m+1):
        S0.append(0)
    
    S0.append([])
    
    Phi = [[tuple(S0)]]
    for k in range(1,n+1):
        Phi_k = []
        for S in Phi[k-1]:
            # Fs = []
            for i in range(0,m):
                F = list(S)
                # print(F)
                F[i] = F[i] + pt1[k-1]
                # 长度为m+2
                F[m] = max(F[0:m])
                
                F[m+1] = F[m+1] + [i+1]
                # Fs.append(F)
                Phi_k.append(tuple(F))
            
        Phi.append(Phi_k)
    return Operation2(Phi,n,m)


def Operation2(Phi,n,m):
    E = [ele[m] for ele in Phi[n]] # 这样方便操作
        # temp 是去除重复之后剩下的
    temp = list(set(E))
    E2 = temp.copy()
    return Phi[n][E.index(min(E2))]
    

Cmax_set = dict()
for u in list(Ps.keys()):
    pt = Ps[u]
    Cmax_set[str(u)] = DP_test(len(pt),pt,len(M))
    
print(Cmax_set)
