#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 01:57:54 2022

@author: xiechen
"""

import pandas as pd
import numpy as np
import gurobipy

# create data set

with open("Gene_Experiment/Gurobi/scheduling_part/Uncertain_Bicriteria_Scheduling/Multiobjective/toy.txt") as f:
    lines = f.readlines()
    M = set(map(int,lines[0].strip('\n').split(',')))
    # jobs set
    J = set(map(int,lines[1].strip('\n').split(',')))
    # scenario set
    U = set([u for u in range(1,10)])
    
    Kj = list(map(int,lines[2].strip('\n').split(','))) #
    Bj = list(map(int,lines[3].strip('\n').split(',')))
    
# varies function
def vary_function(kj,U,bj):
    P = {}
    for u in U:
        p_u = kj*u + bj
        P[u] = (p_u) #
    return P


# Generate Ps
def Generate_Ps(J):
    Ps = []
    for j in J:
        Pj = vary_function(Kj[j], U, Bj[j])
        Ps.append(Pj)
    return Ps

Ps = Generate_Ps(J)
print(Ps)

# make the data package as dataframe
def packageData(J, U , Ps):
    
    index  = list(J)
    columns  = list(U)
    packed_qijr = pd.DataFrame(Ps,index = index, columns = columns)
    return packed_qijr

packed_Ps = packageData(J, U, Ps)
# print(packed_Ps.at[1,2])

# compute the upper bounded time
def compute_upper_time(u):
    utime = 0
    for j in J:
        utime += Ps[j][u]
    return int(utime) #

# add all upper time in the list
def UpperBoundTime(U):
    time_U = {}
    for u in U:
        time_U[u] = compute_upper_time(u)
    return time_U

time_U = UpperBoundTime(U)
print(time_U)

def configuration_model(packed_Ps,u,obj,epsilon):
    '''
    parametrer les contenues communes d'une configuration d'un model
    '''
    #les indices dans un ensemble
    # setPosition = set([ele for ele in range(0,self.taille)])
    # (或者addVars()，如果您希望一次添加多个变量)。变量总是与特定的模型相关联。
    m = gurobipy.Model("Scheduling prob model")
    
    time = [t for t in range(0,time_U[u])]
    # tbs = [i for i in range(0,Up_Cmax+1)]
    I = len(M)
    Ji = len(J)
    
    x = m.addVars(I,Ji,time,vtype=gurobipy.GRB.BINARY)
    Cmax = m.addVar(lb=0.0,vtype=gurobipy.GRB.SEMICONT)
    # Clp = m.addVars(Ji,vtype=gurobipy.GRB.SEMICONT,lb=0.0)
    Clp = m.addVars(Ji,vtype=gurobipy.GRB.INTEGER,lb=0.0)
    if obj == 'f2':    
        m.setObjective(gurobipy.quicksum(Clp[j] for j in J),sense=gurobipy.GRB.MINIMIZE)
    elif obj == 'f1':
        m.setObjective(Cmax)
    else:
        m.setObjective(gurobipy.quicksum(Clp[j] for j in J),sense=gurobipy.GRB.MINIMIZE)
    # index, columns, time
    
    if epsilon > 0:
        m.addConstr(epsilon >= gurobipy.quicksum(Clp[j] for j in J))
        
    m.addConstrs(Cmax >= Clp[j] for j in J)
    
    m.addConstrs(gurobipy.quicksum(x[i,j,t]  
                                   for t in time
                                   for i in M) ==1 for j in J)
    
    m.addConstrs(gurobipy.quicksum(x[i,j,h]
                                   for j in J
                                   for h in range(max(0,int(t-packed_Ps.at[j,u])), t)
                                   ) <=1 
                                         for i in M
                                         for t in time)
    
    m.addConstrs(Clp[j] >= gurobipy.quicksum(x[i,j,t] * (t + packed_Ps.at[j,u])
                                              for t in time
                                              for i in M )
                                              for j in J)
        
    
    m.optimize()
    # Display the results
    print("it took ",m.Runtime,"s to solve")
    print("Objective value: ", m.objVal)
    # Only getting Xijt with positive value.
    X = [(i,j,t) for ((i,j,t),p) in m.getAttr('x', x).items() if p > 0]

    return m.objVal,tuple(X)

def tous_les_min_Cmax_sols():
    set_F1U = {}
    for u in U:
        set_F1U[u] = configuration_model(packed_Ps,u,'f1',0)
    
    return set_F1U

set_F1U = tous_les_min_Cmax_sols()
print(set_F1U)
