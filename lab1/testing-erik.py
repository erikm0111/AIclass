visited = {}
visited[(1,2)] = True
position = (1,2)

print visited
visited.pop(position, None)
print visited

neka_lista = ((1,1),(2,2),(3,3),(4,4))
print len(neka_lista)