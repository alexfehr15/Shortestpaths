#Alex Fehr
#COP4531 programming project 2

import sys, getopt

#algorithm to determine all strongly connected components of a graph

def strongly_connected_components(vertices, edges):
	identified = set()
    	stack = []
    	index = {}
    	boundaries = []

    	for v in vertices:
        	if v not in index:
            		to_do = [('VISIT', v)]

            		while to_do:
                		operation_type, v = to_do.pop()

                		if operation_type == 'VISIT':
                    			index[v] = len(stack)
                    			stack.append(v)
                    			boundaries.append(index[v])
                    			to_do.append(('POSTVISIT', v))
                    			to_do.extend(reversed([('VISITEDGE', w) for w in edges[v]]))
                		elif operation_type == 'VISITEDGE':
                    			if v not in index:
                        			to_do.append(('VISIT', v))
                    			elif v not in identified:
                        			while index[v] < boundaries[-1]:
                            				boundaries.pop()
                		else:
                    			if boundaries[-1] == index[v]:
                        			boundaries.pop()
                        			scc = set(stack[index[v]:])
                        			del stack[index[v]:]
                        			identified.update(scc)
                        			yield scc

#parse through input file and create graph, call functions to analyze graph

def main():
	inputFile = ''
	inputFile = str(sys.argv[1])

	f = open(inputFile, 'r')

	line = ""
	G = {}								#create container for directed graph
	U = {}								#create container for undirected graph

	for line in f.readlines():					#fill up adjacency list (directed & undirected)
		if line[0] <> '#':
			row = line.split('\t')

			if row[0] <> '\n':
				row[0] = int(row[0])
				row[1] = int(row[1])

				if row[0] in G:
					G[row[0]].append(row[1])
				else:
					G[row[0]] = [row[1]]

				if row[0] in U:
					U[row[0]].append(row[1])
				else:
					U[row[0]] = [row[1]]
	
				if row[1] in U:
					U[row[1]].append(row[0])
				else:
					U[row[1]] = [row[0]]

	C = {}								#containers to fascilitate manipulation
	P = []
	D = G
	C2 = {}
	P2 = []
	D2 = U

	for key in G:							
		C[key] = []
		for item in G[key]:
			C[item] = []

	for key in U:
		C2[key] = []
		for item in U[key]:
			C2[item] = []

	for key in C:
		P.append(key)	

	for key in C2:
		P2.append(key)	

	for x in P:
		if x in G:
			pass
		else:
			G[x] = []

	for x in P2:
		if x in U:
			pass
		else:
			U[x] = []

	Q = []								#containers for manipulation
	T = []
	Q2 = []
	T2 = []

	for scc in strongly_connected_components(P, G):			#call algorithm and group connected components
		for x in scc:
			T.append(x)

		Q.append(T)
		T = []

	for scc in strongly_connected_components(P2, U):		#call algorithm and group connected components
		for x in scc:
			T2.append(x)

		Q2.append(T2)
		T2 = []

	max = len(Q[0])
	SCC = Q[0]

	for x in Q:							#determine largest strongly connected component
		if len(x) > max:
			max = len(x)
			SCC = x

	max2 = len(Q2[0])				
	SCC2 = Q2[0]

	for x in Q2:							#determine largest weakly connected component
		if len(x) > max2:
			max2 = len(x)
			SCC2 = x

	total = 0		
	total2 = 0		

	scc = set(SCC)							#create sets for quicker edge counting
	for key in D:
		D[key] = set(D[key])

	scc2 = set(SCC2)						#create sets for quicker edge counting
	for key in D2:
		D2[key] = set(D2[key])

	for x in scc:							#count edges in largest SCC
		for i in D[x]:
			if i in scc:
				total += 1

	for x in scc2:							#count edges in largest WCC
		for i in D[x]:
			if i in scc2:
				total2 += 1

	print "Statistics for given graph is as follows:"		#output results and statistics
	print "Largest WCC"
	print "Nodes - " + str(max2)
	print "Edges - " + str(total2)
	print "Largest SCC"
	print "Nodes - " + str(max)
	print "Edges - " + str(total)		
	print "End"

if __name__ == '__main__':
	main()
