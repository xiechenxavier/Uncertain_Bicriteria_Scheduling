#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:50:46 2022

@author: xiechen
"""
# P1 = vary_function(Kj[0], U, Bj[0])
# P2 = vary_function(Kj[1], U, Bj[1])
# P3 = vary_function(Kj[2], U, Bj[2])
# print(P1)
# print(P2)
# print(P3)

# j = indice + 1
# Ps = [P1,P2,P3]

# def configuration_model(packed_Ps,u):
#     '''
#     parametrer les contenues communes d'une configuration d'un model
#     '''
#     #les indices dans un ensemble
#     # setPosition = set([ele for ele in range(0,self.taille)])
#     # (或者addVars()，如果您希望一次添加多个变量)。变量总是与特定的模型相关联。
#     m = gurobipy.Model("Scheduling prob model")
    
#     time = [t for t in range(0,time_U[u])]
#     # tbs = [i for i in range(0,Up_Cmax+1)]
#     I = len(M)
#     Ji = len(J)
    
#     x = m.addVars(I,Ji,time,vtype=gurobipy.GRB.BINARY)
#     Cmax = m.addVar(lb=0.0,vtype=gurobipy.GRB.SEMICONT)
#     # Clp = m.addVars(Ji,vtype=gurobipy.GRB.SEMICONT,lb=0.0)
#     Clp = m.addVars(Ji,vtype=gurobipy.GRB.INTEGER,lb=0.0)
#     m.setObjective(gurobipy.quicksum(1*Clp[j] for j in J),sense=gurobipy.GRB.MINIMIZE)
#     # index, columns, time
#     m.addConstrs(Clp[j] == t*x[i,j,t] + packed_Ps.at[j,u]
#                                               for t in time
#                                               for i in M 
#                                               for j in J)
#     m.addConstrs(Cmax >= Clp[j] for j in J)
    
#     m.addConstrs(gurobipy.quicksum(x[i,j,t] ==1 
#                                    for t in time
#                                    for i in M) 
#                                             for j in J)
    
    
#     m.addConstrs(gurobipy.quicksum(x[i,j,t] + x[i,j2,s+t] 
#                                    for s in range(0, packed_Ps.at[j,u]) 
#                                    for j2 in J -{j}
#                                    ) <=1 for j in J 
#                                          for i in M
#                                          for t in time)
    
#     m.optimize()
#     # Display the results
#     print("it took ",m.Runtime,"s to solve")
#     print("Objective value: ", m.objVal)
#     # Only getting Xijt with positive value.
#     X = [((i,j,t),p) for ((i,j,t),p) in m.getAttr('x', x).items() if p > 0]

#     return X

# # solution gotten by Solver 
# X= configuration_model(packed_Ps,1)
# print(X)





#     m.addConstrs(gurobipy.quicksum(x[i,j,t] + x[i,j2,s+t] 
#                                    for s in range(0, packed_Ps.at[j,u]) 
#                                    for j2 in J -{j}
#                                    ) <=1 
#                                          for i in M
#                                          for j in J
#                                          for t in range(0, time_U[u]-packed_Ps.at[j,u])
#         
                                  # )


import os

print(os.getcwd())
with open("Gene_Experiment/Gurobi/scheduling_part/Multiobjective/instance.txt") as f:
    lines = f.readlines()
    M = set(map(int,lines[0].strip('\n').split(',')))
    
    J = set(map(int,lines[1].strip('\n').split(',')))
    
    U = set(map(int,lines[2].strip('\n').split(',')))
    
    print(M)
    print(J)
    print(U)

# Machines
M = {0,1}
# Jobs
J = {0,1,2}
# Scenarios
U = {0,1,2,3,4,5,6,7,8}
# Slopes
Kj = {6,3,2}
# bias
Bj = {6,12,18}


# Machines
M = {0,1}
# Jobs
J = {0,1,2,3}
# Scenarios
U = {0,1,2,3,4,5,6,7,8,10,11,12,13,14,15}
# Slopes
Kj = {12,6,4,3}
# bias
Bj = {12,24,36,48}


# Machine
M = {0,1}
# Jobs
J = {0,1,2,3,4,5,6}
# Processing time
P = {1,2,4,5,6,18}

