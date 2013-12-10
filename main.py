import heapq, sys, getopt

#Dijkstra's algorithm, computes shortest path from source node to end node

def dijkstra(adjacency_list, weights, b, e):
	priorityQueue = []     
	distance = {b: 0} 
	distanceQueue = {}   
	pred = {}     
	visited_set = set([b]) 

	for v in adjacency_list.get(b, []):
		distance[v] = weights[b, v]
        	item = [distance[v], b, v]
        	heapq.heappush(priorityQueue, item)
        	distanceQueue[v] = item

    	while priorityQueue:
        	cost, parent, u = heapq.heappop(priorityQueue)
        	if u not in visited_set:
            		pred[u]= parent
            		visited_set.add(u)
            		if u == e:
                		return pred, distance[u]
            		for v in adjacency_list.get(u, []):
                		if distance.get(v):
					if (u, v) in weights:
                    				if distance[v] > weights[u, v] + distance[u]:
                        				distance[v] =  weights[u, v] + distance[u]
                        				distanceQueue[v][0] = distance[v] 
                        				distanceQueue[v][1] = u   
                        				heapq._siftdown(priorityQueue, 0, priorityQueue.index(distanceQueue[v]))
                		else:
                    			distance[v] = weights[u, v] + distance[u]
                    			item = [distance[v], u, v]
                    			heapq.heappush(priorityQueue, item)
                    			distanceQueue[v] = item

    	return {}, -1	#did not find a path

#if graph is undirected, then run this before computing

def transformToUndirected(cost):
    	cost2 = {}
    	for k, w in cost.iteritems():
        	cost2[k] = w
        	cost2[(k[1],k[0])] = w
    	return cost2

#find all paths between two nodes and eliminate ones that are greater than k in length

def find_all_paths(graph, start, end, maximum, path=[]):
      	path = path + [start]

       	if start == end:
           	return [path]
       	if not graph.has_key(start):
            	return []

       	paths = []
       	for node in graph[start]:
            	if node not in path:
                	newpaths = find_all_paths(graph, node, end, maximum, path)
                	for newpath in newpaths:
				if len(newpath) <= maximum + 1:
                    			paths.append(newpath)

       	return paths

#find the minimum cost path among the ones remaining

def findMinPath(cost, paths):
	weight = 0
	maxLength = 0
	minCost = 10000000000
	
	for path in paths:
		maxLength = len(path) - 1
		for i in range(0, maxLength):
			weight += cost[(path[i], path[i+1])]
		if weight < minCost:
			minCost = weight
		weight = 0

	if minCost <> 10000000000:
		return minCost
	else:
		return "none"

#runs with arguments <input_file source_node k>, executes two algorithms on directed or undirected graph

def main():
        inputFile = ''
	outputFile = "output.txt"
        inputFile = str(sys.argv[1])
	sourceNode = str(sys.argv[2])
	kInteger = int(sys.argv[3])

        f = open(inputFile, 'r')
	b = open(outputFile, 'w').close()
	b = open(outputFile, 'w')

        line = ""
        G = {}                                                          #create container for directed graph
        U = {}                                                          #create container for undirected graph
	cost = {}
	edges = set()

        for line in f.readlines():                                      #fill up adjacency list (directed & undirected)
                if line[0] <> '#':
                        row = line.split(' ')

			if (len(row) == 1) and (row[0] <> '\n'):
				if str((row[0])[0]) == 'D':
					key = str((row[0])[0])
				else:
					key = str((row[0])[0]) + str((row[0])[1])

                        elif row[0] <> '\n':
                                row[0] = str(row[0])
                                row[1] = str(row[1])
				row[2] = int(row[2])

				if row[0] not in edges:
					edges.add(row[0])
				if row[1] not in edges:
					edges.add(row[1])

				if key == 'D':
                                	if row[0] in G:
                                        	G[row[0]].append(row[1])
                                	else:
                                        	G[row[0]] = [row[1]]
					
					cost[(row[0], row[1])] = row[2]
					
				elif key == "UD":
                                	if row[0] in U:
                                        	U[row[0]].append(row[1])
                                	else:
                                        	U[row[0]] = [row[1]]

                                	if row[1] in U:
                                        	U[row[1]].append(row[0])
                                	else:
                                        	U[row[1]] = [row[0]]

					cost[(row[0], row[1])] = row[2]

	counter = len(edges)
	if key == 'D':				#decide whether directed or undirected
		adj = G
	elif key == 'UD':
		cost = transformToUndirected(cost)
		adj = U

	b.write("Dijkstra\n")
	b.write("Source : " + sourceNode + '\n')
	b.write("Node " + sourceNode + " : " + str(0) + '\n')
	for t in edges:
		if t <> sourceNode:
			predecessors, min_cost = dijkstra(adj, cost, sourceNode, t)
			if min_cost == -1:
				b.write("Node " + t + " : " + "none" + '\n')
			else:
				b.write("Node " + t + " : " + str(min_cost) + '\n')
	b.write("End Dijkstra\n")

	#now for the shortest reliable paths algorithm

	b.write("Shortest Reliable Paths Algorithm\n")
	b.write("Integer k : " + str(kInteger) + " Source : " + sourceNode + '\n')
	if (kInteger > (counter - 1)):
		b.write("Node " + sourceNode + " : integer larger than |V| - 1" + '\n')
	else:
		b.write("Node " + sourceNode + " : " + str(0) + '\n')
	for t in edges:
		if t <> sourceNode:
			paths = find_all_paths(adj, sourceNode, t, kInteger)
			if (kInteger > (counter - 1)):
				b.write("Node " + t + " : integer larger than |V| - 1\n")
			else:
				b.write("Node " + t + " : " + str(findMinPath(cost, paths)) + '\n')
	b.write("End Shortest Reliable Paths Algorithm\n")

	f.close()
	b.close()

if __name__=='__main__':
	main()
