#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:55:51 2022

@author: xiechen
"""
import pandas as pd
import numpy as np
import gurobipy

# create data set

with open("Gene_Experiment/Gurobi/scheduling_part/Uncertain_Bicriteria_Scheduling/Multiobjective/toy2.txt") as f:
    lines = f.readlines()
    M = set(map(int,lines[0].strip('\n').split(',')))
    # jobs set
    J = set(map(int,lines[1].strip('\n').split(',')))
    # scenario set
    # U = set(map(int,lines[2].strip('\n').split(',')))
    U = set([u for u in range(1,2)])
    
    Kj = list(map(int,lines[2].strip('\n').split(',')))
    Bj = list(map(int,lines[3].strip('\n').split(',')))
    
# varies function
def vary_function(kj,U,bj):
    P = {}
    for u in U:
        p_u = kj*u + bj
        P[u] = p_u
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
    return utime

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
                                   for h in range(max(0,t-packed_Ps.at[j,u]), t)
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
        if u == 0:
            continue
        set_F1U[u] = configuration_model(packed_Ps,u,'f1',0)
    
    return set_F1U

def tous_les_min_TFT_sols():
    set_F2U = {}
    for u in U:
        if u == 0:
            continue
        set_F2U[u] = configuration_model(packed_Ps, u, 'f2',0)
    
    return set_F2U
    
set_F1U = tous_les_min_Cmax_sols()
set_F2U = tous_les_min_TFT_sols()
# print(set_F1U)
# print(set_F2U)

# set a function f2(x1*,u): compute the objective value of f2 for x1* 
def Generate_Cjs(sols,u):
    Cjs = {}
    for tup in sols:
        j = tup[1]
        t = tup[2]
        Cjs[j] = t + Ps[j][u]
    return Cjs

def f2(sols,u):
    # ([((0, 0, 0), 1.0), ((0, 1, 6), 1.0), ((1, 2, 0), 1.0)])
    # Ps[j][u]
    Cjs = Generate_Cjs(sols, u)
    return sum(Cjs.values())

def F2(set_F1U):
    
    F2U = {}
    for u in U:
        min_x1_sols = set_F1U[u][1]
        F2U[u] = f2(min_x1_sols,u)
    
    return F2U

F2U = F2(set_F1U)
print(F2U)

def f1(sols, u):
    '''
    This function is used to compute the objective value of f1
    input : 
        sols ex:((0, 0, 15), (0, 1, 0), (1, 2, 0))
        u: scenario
        
    '''
    Cjs = Generate_Cjs(sols,u)
    
    return max(Cjs.values())
        
def possible_Pareto_sols(set_F1U,F2U,u):
    
    epsilon_u = F2U[u]
    set_PO_u = {}
    
    while epsilon_u >= set_F2U[u][0]:
        f1_eps = configuration_model(packed_Ps,u,'f1',epsilon_u)
        set_PO_u[(epsilon_u,f1_eps[0])] = f1_eps[1]
        epsilon_u -= 1
    return set_PO_u
    
Pareto_sols_1 = possible_Pareto_sols(set_F1U, F2U, 1)

# drop repeative solutions
print(set(Pareto_sols_1.values()))

# continuite drop dominated solutions
def Pareto_set(u):
    '''
    objective:
    return a pareto set through dropping all dominated solutions
    from a possible pareto solutions

    '''
    Pareto_sols_1 = set(possible_Pareto_sols(set_F1U, F2U, u).values())
    Pareto_sols_2 = Pareto_sols_1
    for x1 in Pareto_sols_1:
        for x2 in Pareto_sols_1-{x1}:
            f1_x1_u = f1(x1,u)
            f2_x1_u = f2(x1,u)
            f1_x2_u = f1(x2,u)
            f2_x2_u = f2(x2,u)
            
            if (f1_x1_u <= f1_x2_u and f2_x1_u <= f2_x2_u) and(f1_x1_u < f1_x2_u or f2_x1_u < f2_x2_u):
                
                Pareto_sols_2 = Pareto_sols_2 - {x2}
            
    return Pareto_sols_2
            
def all_scenario_Pareto_set(U):
    
    Pareto_setU = {}
    for u in U:
        if u == 0:
            continue
        Pareto_setU[u] = Pareto_set(u)
        
    return Pareto_setU

print(all_scenario_Pareto_set(U))  
    
    
    
    

