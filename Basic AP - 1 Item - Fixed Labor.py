# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 17:51:54 2021

@author: Amirreza
"""

from pyomo.environ import *

Model = ConcreteModel()


#Parameters
t=6
dt = [ 0, 1000, 1200, 1400, 1600, 1400, 1000] #Demand
I0 = 200 #Initial Inventory
B0 = 0 #Initial Shortage
WN = 5 #Normal Time Wage
WE = 8 #Extra Time Wage
IC = 2 #Inventory Cost per Unit per Month
BC = 7 #Shortage Cost per Unit per Month
EC = 700 #Employment Cost
FC = 500 #Firing Cost
PT = 3 #Production Time per unit
L = 21 #Initial Labor
TH = 160 #Available Time per Person
EH = TH*0.4 #Available Extra Time per Person
TTH = TH * L
TEH = EH * L
PC = 1 #production Cost

#Set

Model.IDX = RangeSet(t)

#Var

Model.x = Var(Model.IDX , within = NonNegativeIntegers) #Production
Model.I = Var(Model.IDX , within = NonNegativeIntegers) #Inventory
Model.w = Var(Model.IDX , within = NonNegativeIntegers) #Work Time
Model.O = Var(Model.IDX , within = NonNegativeIntegers) #Extra Work Time

#Objective

Model.obj = Objective( expr = sum( (PC*Model.x[i+1] + IC*Model.I[i+1] ) for i in range(t)) + sum( (WN*Model.w[i+1] + WE*Model.O[i+1]) for i in range(t))  , sense= minimize )

#Constraint

Model.ST = ConstraintList()

for i in range(t):
    if i == 0:
        Model.ST.add( I0 + Model.x[i+1] - Model.I[i+1] == dt[i+1] )
    else:
        Model.ST.add( Model.I[i] + Model.x[i+1] - Model.I[i+1] == dt[i+1] )
    
    Model.ST.add( PT * Model.x[i+1] <= Model.w[i+1] + Model.O[i+1] )
    Model.ST.add( Model.w[i+1] <= TTH )
    Model.ST.add( Model.O[i+1] <= TEH )
    
solver = SolverFactory('cplex')
solver.solve(Model)
display(Model)
    

