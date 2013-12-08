import heapq, sys, getopt

#Dijkstra's algorithm, computes shortest path from source node to end node

def dijkstra(adj, costs, s, t):
	Q = []     		#priority queue
	d = {s: 0} 		#vertex (minimal distance)
	Qd = {}    		#[d[v], parent_v, v]
	p = {}     		#predecessor
	visited_set = set([s]) 	#set of visited vertices

	for v in adj.get(s, []):
		d[v] = costs[s, v]
        	item = [d[v], s, v]
        	heapq.heappush(Q, item)
        	Qd[v] = item

    	while Q:
        	cost, parent, u = heapq.heappop(Q)
        	if u not in visited_set:
            		p[u]= parent
            		visited_set.add(u)
            		if u == t:
                		return p, d[u]
            		for v in adj.get(u, []):
                		if d.get(v):
					if (u, v) in costs:
                    				if d[v] > costs[u, v] + d[u]:
                        				d[v] =  costs[u, v] + d[u]
                        				Qd[v][0] = d[v]    #decrease the key
                        				Qd[v][1] = u       #update predecessor
                        				heapq._siftdown(Q, 0, Q.index(Qd[v]))
                		else:
                    			d[v] = costs[u, v] + d[u]
                    			item = [d[v], u, v]
                    			heapq.heappush(Q, item)
                    			Qd[v] = item

    	return None

#if graph is undirected, then run this before computing

def make_undirected(cost):
    	ucost = {}
    	for k, w in cost.iteritems():
        	ucost[k] = w
        	ucost[(k[1],k[0])] = w
    	return ucost

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
				if len(newpath) <= maximum:
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
        inputFile = str(sys.argv[1])
	sourceNode = str(sys.argv[2])
	kInteger = int(sys.argv[3])

        f = open(inputFile, 'r')

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
		cost = make_undirected(cost)
		adj = U

	print "Dijkstra"
	print "Source : " + sourceNode
	print "Node " + sourceNode + " : " + str(0)
	for t in edges:
		if t <> sourceNode:
			predecessors, min_cost = dijkstra(adj, cost, sourceNode, t)
			print "Node " + t + " : " + str(min_cost)
	print "End Dijkstra\n"

	#now for the shortest reliable paths algorithm

	print "Shortest Reliable Paths Algorithm"
	print "Integer k : " + str(kInteger) + " Source : " + sourceNode
	if (kInteger > (counter - 1)):
		print "Node " + t + " : integer larger than |V| - 1"
	else:
		print "Node " + sourceNode + " : " + str(0)
	for t in edges:
		if t <> sourceNode:
			paths = find_all_paths(adj, sourceNode, t, kInteger)
			if (kInteger > (counter - 1)):
				print "Node " + t + " : integer larger than |V| - 1"
			else:
				print "Node " + t + " : " + str(findMinPath(cost, paths))
	print "End Shortest Reliable Paths Algorithm"

if __name__=='__main__':
	main()
