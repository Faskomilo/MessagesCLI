A= {}
B = {}
A = {'x':1,'y': 2,'z':3}
B = {   'w' : 10,   'x' : 11,   'y' : 2 } 
for x & y in set(A) & set(B):
    if x == y:
        print x