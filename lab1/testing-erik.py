visited = {}
visited[(1,2)] = True
position = (1,2)

print visited
visited.pop(position, None)
print visited