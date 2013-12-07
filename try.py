import heapq, sys, getopt

def dijkstra(adj, costs, s, t):
	''' Return predecessors and min distance if there exists a shortest path 
	from s to t; Otherwise, return None '''
	Q = []     # priority queue of items; note item is mutable.
	d = {s: 0} # vertex -> minimal distance
	Qd = {}    # vertex -> [d[v], parent_v, v]
	p = {}     # predecessor
	visited_set = set([s])

	for v in adj.get(s, []):
		d[v] = costs[s, v]
        	item = [d[v], s, v]
        	heapq.heappush(Q, item)
        	Qd[v] = item

    	while Q:
        	#print Q
        	cost, parent, u = heapq.heappop(Q)
        	if u not in visited_set:
            		#print 'visit:', u
            		p[u]= parent
            		visited_set.add(u)
            		if u == t:
                		return p, d[u]
            		for v in adj.get(u, []):
                		if d.get(v):
					if (u, v) in costs:
                    				if d[v] > costs[u, v] + d[u]:
                        				d[v] =  costs[u, v] + d[u]
                        				Qd[v][0] = d[v]    # decrease key
                        				Qd[v][1] = u       # update predecessor
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

def main():
        inputFile = ''
        inputFile = str(sys.argv[1])

        f = open(inputFile, 'r')

        line = ""
        G = {}                                                          #create container for directed graph
        U = {}                                                          #create container for undirected graph
	cost = {}

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

	print G
	print U
	print cost

    	'''
    	adj = { 'A': ['B','C','F'],
            	'B': ['A','C','D'],
            	'C': ['A','B','D','F'],
            	'D': ['B','C','E','F'],
            	'E': ['D','F','G'],
            	'F': ['A','C','E','G'],
            	'G': ['D','E','F']} '''

    	temp = { ('A','B'):7,
            	('A','C'):9,
            	('A','F'):14,
            	('B','C'):10,
            	('B','D'):15,
            	('C','D'):11,
            	('C','F'):2,
            	('D','E'):6,
            	('E','F'):9,
            	('D','G'):2,
            	('E','G'):1,
            	('F','G'):12}

	print temp
    	cost = make_undirected(cost)

	s = 'B'
	if key == 'D':
		adj = G
	elif key == 'UD':
		adj = U

	print "Dijkstra"
	print "Source : " + s
	print "Node " + s + " : " + str(0)
	for t in adj:
		if t <> s:
			predecessors, min_cost = dijkstra(adj, cost, s, t)
			print "Node " + t + " : " + str(min_cost)
	print "End Dijkstra"

if __name__=='__main__':
	main()