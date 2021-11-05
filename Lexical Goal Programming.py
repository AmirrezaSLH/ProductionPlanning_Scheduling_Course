# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 18:57:20 2021

@author: Amirreza
"""

from pyomo.environ import *

M = ConcreteModel()   

mat = {}
mat[1] = 5
mat[2] = 10
mat[3] = 15

time = {}
time[1]=10.5
time[2]=15
time[3]=17

prof = {}
prof[1]= 50
prof[2]= 100
prof[3]= 75

minproduction ={}
minproduction[1]=5
minproduction[2]=7
minproduction[3]=5

TTime = 400
Tmat = 300
Eprofit = 3000

#IDX

M.IDX = RangeSet(3)  # 1 Chair 2 Table 3 Bench
M.GP = RangeSet(2) # 1 - 2 +

#Parameter

M.material = Param( M.IDX, initialize=mat , default=0)
M.time = Param( M.IDX, initialize=time , default=0)
M.profit = Param( M.IDX, initialize=prof , default=0)
M.minproduction = Param( M.IDX, initialize=minproduction , default=0)

M.TTime = Param( initialize=TTime , default=0)
M.Tmat = Param( initialize=Tmat , default=0)
M.Eprofit = Param( initialize=Eprofit , default=0)


#variable

M.x = Var( M.IDX , within = NonNegativeIntegers)
M.t = Var( M.GP, within = NonNegativeReals)
M.p = Var( M.GP, within = NonNegativeReals)
M.m = Var( M.GP, within = NonNegativeReals)

#Objective

M.objp = Objective(expr = M.p[2], sense = minimize) 
#M.objt = Objective(expr = M.t[2], sense = minimize) 
#M.objm = Objective(expr = M.m[2], sense = minimize) 

#Constraint

M.ST = ConstraintList()
#M.ST.add(M.t[2] <= 40)

M.ST.add(sum( M.x[i]*M.time[i] for i in M.IDX) + M.t[1] - M.t[2] == M.TTime)
M.ST.add(sum( M.x[i]*M.material[i] for i in M.IDX) + M.m[1] - M.m[2] == M.Tmat)
M.ST.add(sum( M.x[i]*M.profit[i] for i in M.IDX) + M.t[1] - M.t[2] == M.Eprofit)

for i in M.IDX:
    M.ST.add(M.x[i] >= M.minproduction[i])

solverpart1 = SolverFactory('cplex')
solverpart1.solve(M)
display(M)

print("----------------GOAL2---------------")
#--------------------------------Goal 2
M2 = M
M2.ST.add( sum( M2.x[i]*M2.profit[i] for i in M.IDX) >= M.Eprofit+ M.p[2] - M.p[1])
M2.objp = Objective(expr = M2.t[2], sense = minimize)

solverpart1 = SolverFactory('cplex')
solverpart1.solve(M2)
display(M2)

print("----------------GOAL3---------------")
#--------------------------------Goal 3
M3 = M
M3.ST.add( sum( M2.x[i]*M2.time[i] for i in M.IDX) <= M.TTime+ M2.t[2] - M2.t[1])
M3.objp = Objective(expr = M3.m[2], sense = minimize)

solverpart1 = SolverFactory('cplex')
solverpart1.solve(M3)
display(M3)


print("----------------Final Results---------------")

for i in M.IDX:
        print("X[",M.IDX[i], "]:", M3.x[i].value)
  
print("profit:", sum(M3.x[i].value*M3.profit[i] for i in M3.IDX))
print("worktime:", sum(M3.x[i].value*M3.time[i] for i in M3.IDX))
print("consumedmaterial:", sum(M3.x[i].value*M3.material[i] for i in M3.IDX))

#print( M.Eprofit+ M.p[2].value - M.p[1].value ) 
#print(M.TTime+ M2.t[2].value - M2.t[1].value)


