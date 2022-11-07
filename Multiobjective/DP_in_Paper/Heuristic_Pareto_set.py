#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 04:59:28 2022

@author: xiechen
"""
import pandas as pd
import numpy as np

# create data set

with open("Gene_Experiment/Gurobi/scheduling_part/Uncertain_Bicriteria_Scheduling/Multiobjective/instances/toy6.txt") as f:
    lines = f.readlines()
    M = set(map(int,lines[0].strip('\n').split(',')))
    # jobs set
    J = set(map(int,lines[1].strip('\n').split(',')))
    # scenario set
    U = set([u for u in range(1,30)])
    
    Kj = list(map(float,lines[2].strip('\n').split(','))) #
    Bj = list(map(int,lines[3].strip('\n').split(',')))
    
# varies function

# Generate Ps
def Generate_Ps(J):
    Ps = {}
    for u in range(1,30):
        Ps[u] = []
        for j in J:
            Ps[u].append(Kj[j] * u + Bj[j])

    return Ps

Ps = Generate_Ps(J) # Ps is the table of processing time of all jobs in every scenario
print(Ps)
    
# Generate Ps2
# def Generate_Ps2(J):
#     Ps = {}
#     for u in range(0, 5):
#         Ps[u] = []
#         for j in J:
#             Ps[u].append(Kj[j]+u*0.1)
#     return Ps
# Ps = Generate_Ps2(J) 
# print(Ps)
    
# def Generate_Ps2(J):
#     Ps = {}
#     for u in range(1, 9):
#         Ps[u] = []
#         for j in J:
#             if j != len(J)-1:
#                 Ps[u].append(Kj[j]+u)
#             else:
#                 Ps[u].append(Kj[j])
#     return Ps
# Ps = Generate_Ps2(J) 
# print(Ps)
# def Generate_Ps2(J):
#     Ps = {}
#     for u in range(1, 9):
#         Ps[u] = []
#         for j in J:
#             Ps[u].append(Kj[j]+u)

#     return Ps
# Ps = Generate_Ps2(J) 
# print(Ps)

def DP_test(n,pt1,m):
    '''

    Parameters
    ----------
    n : integer
        the number of jobs.
    pt1 : A list (integer or float)
        processing time list of all jobs.
    m : integer
        the number of machines.

    Returns
    -------
    Set
        all information of pareto solutions : 
            - load of each machine
            - bi-objective values
            - schedule.
    '''
    # S0 
    S0 = []
    for i in range(0, m+2): # bi-objective
        S0.append(0)
    
    S0.append([])
    
    Phi = [[tuple(S0)]]
    for k in range(1,n+1):
        Phi_k = []
        for S in Phi[k-1]:
            for i in range(0,m):
                F = list(S)
                F[i] = F[i] + pt1[k-1]
                # To update total completion time
                F[m] = F[m]+ F[i]
                # To update Cmax
                F[m+1] = max(F[0:m])
                # To update the partial schedule
                F[m+2] = F[m+2] + [i+1]
                # add state F in the set
                Phi_k.append(tuple(F))
            
        Phi.append(Phi_k)
    return Operation2(Phi,n,m)

def Operation2(Phi,n,m):
    # Only consider bi-objective values
    E = [(ele[m],ele[m+1]) for ele in Phi[n]]
        # E2 is to eliminate duplication in E
    E2 = list(set(E))
    E2.sort()
    # first element as the initial last index of FP 
    z1 = E2[0]
    FP = {z1}
    last = z1 
    for i in range(1,len(E2)):
        if E2[i][0] > last[0]:
            if E2[i][1] < last[1]:
                FP.add(E2[i])
                last = E2[i]
    # Because only one symmetry needs to be considered, 
    # the index corresponding to the value of FP can be used.
    return [Phi[n][E.index(nd_val)] for nd_val in FP]

# b = [1, 2, 4, 5, 6, 18]
# print(DP_test(6,b,2))

Pareto_set = dict()
for u in list(Ps.keys()):
    pt = Ps[u]
    Pareto_set[str(u)] = DP_test(len(pt),pt,len(M))
    
print(Pareto_set)
