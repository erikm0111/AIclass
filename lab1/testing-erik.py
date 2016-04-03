"""
visited = {}
visited[(1,2)] = True
position = (1,2)

print visited
visited.pop(position, None)
print visited

neki_tuple = ((1,1),(2,2),(3,3),(4,4))
neka_lista = [(neki)]
print len(neka_lista)
"""
#p =lambda x: x*2
#print p(2)
import sys
position = ((2,3),"Ludilo")
x,y = position[0]
print x,y
print sys.maxint