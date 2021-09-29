'''
This holds groups for the combinatoric optimization of their data. For reasons involving professionalism we're going to refer to the items as accounts and prose
Author: Robyn Proffer September 2018
'''

#used libraries and modules
from Payment import payment, prioritywrapper, paymentPlus
from queue import PriorityQueue
from copy import deepcopy
class Account:
    keyNumber: str
    prose: list
    Credit: float
    totaldebt: float
    headers: list
    solution: list
    SolutionValue: float
    payments: list
    possiblepayments: list
    tries: int
    Chill: int
    viableEntries: list
    creditlist: list
    prevSol: float
    check: float
    
    def __init__(self, accNum, headings):
        self.keyNumber = accNum
        self.tries = 0
        self.check = 0
        self.Chill = 0
        self.prose = []
        self.Credit = 0
        self.totaldebt = 0
        self.headers = headings
        self.solution = []
        self.SolutionValue = 0
        self.possiblepayments = []
        self.viableEntries = []
        self.creditlist = []
        self.prevSol = -1
        
    def addEntry(self, entry):
        #print(entry)
        self.prose.append(entry)
        self.Credit = abs(float(entry[self.headers['Credit balance']]))
        if abs(float(entry[self.headers['Open']])) <= self.Credit and float(entry[self.headers['Open']]) > 0:   
            self.viableEntries.append(entry)
            self.check+=abs(float(entry[self.headers['Credit balance']]))
            newpayment = payment(entry[self.headers['OT']]+entry[self.headers['PRO']], float(entry[self.headers['Open']]), self.Credit, entry)
            newpayment.plan.append(newpayment)
            self.possiblepayments.append(newpayment)
        if float(entry[self.headers['Open']]) > 0:
            self.totaldebt = self.totaldebt + float(entry[self.headers['Open']])
        if float(entry[self.headers['Open']]) < 0:
            newpayment = payment(entry[self.headers['OT']]+entry[self.headers['PRO']], float(entry[self.headers['Open']]), self.Credit, entry)
            self.creditlist.append(newpayment)
    
    def getPlan(self):
        plan = []
        #print(str(self.totaldebt)+'/'+str(self.Credit))
        if self.totaldebt<=self.Credit:
            for element in self.viableEntries:
                plan.append([self.keyNumber, element[self.headers['OT']]+element[self.headers['PRO']], element[self.headers['Open']], self.totaldebt, self.totaldebt, self.Credit])
            remnant = self.Credit - self.totaldebt
            for element in self.creditlist:
                v = element.amount
                if remnant > 0: #I don't really need this but setting the amount to something new every time seems bad
                    #print(element.amount)
                    #print('+' + str(remnant))                    
                    element.amount = min(0, element.amount + remnant)
                    remnant = max(0, remnant-abs(element.amount))
                    #print(element.amount)
                plan.append([self.keyNumber, element.pro, element.amount, self.totaldebt, self.SolutionValue, self.Credit, v])
            return plan
        else:
            print("thinking")
            solved = self.plan()
            for element in self.solution:
                plan.append([self.keyNumber, element.pro, element.amount, self.totaldebt, self.SolutionValue, self.Credit])
            #remnant = self.Credit - self.SolutionValue
            #remnant = remnant - self.SolutionValue
            remnant = self.SolutionValue
            for element in self.creditlist:
                if remnant > 0:
                    #print(element.amount)
                    #print('+' + str(remnant))
                    element.amount = min(0, element.amount + remnant)
                    remnant = max(0, remnant-abs(element.amount))
                    #print(element.amount)
                plan.append([self.keyNumber, element.pro, element.amount, self.totaldebt, self.SolutionValue, self.Credit])
            return plan
    
    def _calculateHeuristic(self, candidate):
        #print(candidate.planValue)
        return self.Credit - candidate.planValue
    
    def _CheckConditions(self): #check for victory
        if self.tries%len(self.possiblepayments) == 0:
            self.Chill+=1
        #if self.SolutionValue >= self.Credit - self.Chill:
        print(self.Credit - ((self.Chill/self.Credit)*100))
        if self.SolutionValue >= self.Credit - ((self.Chill/self.Credit)*100):
            return True
        return False
    '''
    I need to figure out how to relax it enough to let roland through without impacting the others. Or maybe reset the used 
    combinations after a certain point? stop storing unuseful lines? <--I like this one. Discard the worst five every
    few additions/only store a given number of helpful goes. It seems to maybe get caught in an infinite loop.
    Is that what's happening? Check what happens during the continue/or too big check. That might shed some light on the subject. 
    It might be trying to use the same cell again and again.
    '''
    def plan(self): 
        start = payment('noPro', 0, 0, None) #build a start node, setting the values to all 0. 
        q = PriorityQueue() #the fringe to search.
        q.put(prioritywrapper(0, start)) #initially, we only know the start node, which is effectively just a marker
        count = 0
        for item in self.possiblepayments:
            print(item.amount)
            print(item.entry)
        while q.empty() != True:
            current = q.get().item #get the next most valuable candidate
            #print(current.amount)
            for item in self.possiblepayments: #look at all the options
                print(self.tries)
                print(self.Chill)
                if self.SolutionValue == self.prevSol:
                    self.tries+=1             
                if self._CheckConditions():
                    q = None
                    return 1
                if current.planValue == 0:
                    potential = item.amount+current.amount #candidate cost
                else:
                    potential = item.amount+current.planValue
                #print('candidate solution value: ' + str(potential) + ' | cap: ' + str(self.Credit) + ' | debt: '+ str(self.totaldebt))
                if item.pro in current.pros or potential > self.Credit:
                    continue #this candidate does not lend itself to a solution or it's already a part of the best solution for the current pro, next please
                if potential > item.planValue: #okay but do I need the smallest value here or the biggest? I'm trying to maximize my cost here.
                    x = paymentPlus(item) #save the state of this item
                    x.planValue = deepcopy(potential) #switch out value of the plan for the value of a better plan
                    x.previous = deepcopy(current) #linear path, not very useful
                    x.plan = deepcopy(current.plan) #found better plan involving this item
                    x.plan.append(item) #add this item to itself
                    x.pros = deepcopy(current.pros)
                    x.pros.append(item.pro)
                    #self.possiblepayments.append(x) #allow for adding this state onto future states?
                    if x.planValue > self.SolutionValue: #is this new solution better than the current one?
                        self.tries = 0
                        self.SolutionValue = x.planValue #switch out solution value for a better one
                        self.solution = x.plan #switch out the current solution for a better one
                        #if self.SolutionValue == self.Credit:
                            #return 1 #we did it!
                    f = (potential + self._calculateHeuristic(x)) #Determine the value of this option
                    #f = 1/(potential + self._calculateHeuristic(x)) #Determine the value of this option
                    t = prioritywrapper(f, x)
                    q.put(t)
                    print('current value solved for: ' + str(self.SolutionValue) + ' | cap: ' + str(self.Credit) + ' | debt: '+ str(self.totaldebt))
                self.prevSol = deepcopy(self.SolutionValue)
        q = None
        return 0          
                
                
