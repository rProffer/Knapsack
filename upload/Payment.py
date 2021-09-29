'''
The purpose of this class is to hold the A* data for some pros for the purposes of optimizing credit usage when paying off old bills
Robyn Proffer
August 2018
'''
## TODO

##

#used libraries and modules
from dataclasses import dataclass, field
from typing import Any
from copy import deepcopy
class payment:
    pro: str
    amount: float #node cost
    previous: Any #the previous node in the stack
    plan: list #selected
    planValue: float
    cost: float #cost of getting here. G-Score
    entry: list
    pros: list
    def __init__(self, pro, amount, credit, entry):
        self.pro = pro
        self.entry = entry
        self.previous = None
        self.plan = []
        self.planValue = 0
        self.cost = 0 #credit*credit*credit #set to infinity. maybe set to zero and find ones bigger?
        self.amount = amount
        self.pros = [pro] #mostly for debugging purposes
        
@dataclass(order = True)
class prioritywrapper:
        priority: float
        item: Any=field(compare = False)

class paymentPlus: #freezes a copy of payment in state for stable decisionmaking
    pro: str
    amount: float #node cost
    previous: Any #the previous node in the stack
    plan: list #selected
    planValue: float
    cost: float #cost of getting here. G-Score
    entry: list
    pros: list
    def __init__(self, item):
        self.pro = item.pro
        self.entry = item.entry
        self.previous = deepcopy(item.previous)
        self.plan = deepcopy(item.plan)
        self.planValue = deepcopy(item.planValue)
        self.cost = deepcopy(item.cost) #credit*credit*credit #set to infinity. maybe set to zero and find ones bigger?
        self.amount = item.amount
        self.pros = deepcopy(item.pros) #mostly for debugging purposes
        