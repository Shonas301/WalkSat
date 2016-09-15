#!/usr/bin/python

import sys
import random
import json
import timeit
from ast import literal_eval

class WalkSAT:
    defined = 0     #contains whether or not file has reached p
    clauses = []    #the actual clauses parsed out
    numVar = 0      #number of variables
    numClause = 0   #number of clauses
    T = []          #truth statement
    literals = {}   #where each literal is located, by clause
    p = .2          #temporary test, is assigned later by argument
    timeLimit = 10000000000 #changed later by argument
    falseClauses = [] #list of all clauses not satisfied by T
    numSatisfiedLitsPerClause = {} #verbatim from slides
    start = 0       #start time
    stop = 0        #stop time
    flips = 0       #number of flips made

"""
    @param: self

    Description:
    Driver for the WalkSAT problem."""
    def main(self):
        self.start = timeit.default_timer()     
        self.readFile()
        self.createContainingClauses()
        self.SATLoop()
        self.stop = timeit.default_timer()
        print("Runtime:", self.stop-self.start)
        print("Flips made:", self.flips)
        
    def SATLoop(self):
        self.setFalseClauses()
        while(self.notComplete()):
            C = self.getClause()
            r = random.random()
            if (r > self.p):
                self.pickVar(C)
            else:
                x = random.randint(1,self.numVar) - 1
                self.flip(x)
            self.setFalseClauses()
            if(timeit.default_timer() - self.start > self.timeLimit):
                print("UNKNOWN")
                print("Flips made:", self.flips)
                sys.exit()
        print("SATISFIABLE")
        print("Solution",self.T)

    def readFile(self):
        fileName = sys.argv[1]
        self.timeLimit = float(sys.argv[2])
        self.p = float(sys.argv[3])
        #print (sys.argv[1])
        with open(fileName, 'r') as f:
            data = f.readlines()
        for line in data:
            words = line.split()
            if (words[0] is '%'):
                break
            if (words[0] is 'c'):
                continue
            elif(words[0] is not 'c' and self.defined is not 1):
                self.defined = 1
                self.numVar = int(words[2])
                self.numClause = int(words[3])
            else:
                temp = []
                for x in words:
                    y = int(x)
                    if y is not 0:
                        temp.append(int(x))
                self.clauses.append(temp)
        for x in range(1,self.numVar+1):
            choice = [-1,1]
            self.T.append(x * random.choice(choice))

    def createContainingClauses(self):
        for x in range(1,self.numVar+1):
            self.literals[x] = []
            self.literals[x*-1] = []
            for instance in self.clauses:
                if x in instance:
                    self.literals[x].append(instance)
                if x*-1 in instance:
                    self.literals[x*-1].append(instance)

    def getClause(self):
        try:
            c = random.choice(self.falseClauses)
        except (IndexError):
            print("Solved")
            print(self.T)
            sys.exit()
        return random.choice(self.falseClauses)


    def setFalseClauses(self):
        self.falseClauses = []
        z = 0
        for instance in self.clauses:
            for x in self.T:
                if x in instance:
                    z += 1
            if z is 0:
                self.falseClauses.append(instance)
            self.numSatisfiedLitsPerClause[str(instance)] = z    #edit
            z = 0

    def notComplete(self):
        z = 0
        for instance in self.numSatisfiedLitsPerClause.keys():
            if (self.numSatisfiedLitsPerClause[instance] ==0):
                z+=1
        if z is 0:
            return False
        else:
            return True
    
    def flip(self,x):
        self.flips +=1
        self.T[x] = self.T[x] * -1
        for instance in self.numSatisfiedLitsPerClause.keys():
            data = literal_eval(instance)
            if str(x) in instance:
                if (self.numSatisfiedLitsPerClause[instance] > 0):
                    self.numSatisfiedLitsPerClause[instance] -= 1
                if(self.numSatisfiedLitsPerClause[instance] == 0):
                    self.falseClauses.append(data)
            if str(x * -1) in instance:
                self.numSatisfiedLitsPerClause[instance] += 1
                if(self.numSatisfiedLitsPerClause[instance] - 1 == 0):
                    self.falseClauses.remove(data)
    
    def pickVar(self, C):
        max_v = -1000
        y = 0
        for x in C:
            make = 0
            breakVar = 0
            for y in self.literals[x]:
                if self.numSatisfiedLitsPerClause[str(y)] is 0:
                    make += 1
            for y in self.literals[x*-1]:
                if self.numSatisfiedLitsPerClause[str(y)] is 1:
                    breakVar +=1
            v = make - breakVar
            if max_v < v:
                max_v = v
                position = abs(x) - 1
        self.flip(position)



c1 = WalkSAT()
c1.main()
