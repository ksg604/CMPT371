
from collections import defaultdict
import math


class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self,value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance


first_node = None
Q = None

# Specify graph properties by taking an input file from the user.
input_file_name = input("Enter input file name: ")


with open(input_file_name, "r") as input_file:
    num_lines = sum(1 for line in input_file)

#constructGraph will determine the network properties by reading the input file
def constructGraph():

    i = 0
    graph = Graph()

    with open(input_file_name, "r") as input_file:

        while i < num_lines:

            #Read the first line in the input file.
            if i == 0:
                line1 = input_file.readline()
                line1_arr = line1.split()

                num_nodes = int(line1_arr[0])
                num_links = int(line1_arr[1])

                i += 1

            #Read the second line in the input file. (list of node names)
            if i == 1:
                line2 = input_file.readline()
                node_names = line2.split()

                for node_name in node_names:
                    graph.add_node(node_name)

                global Q
                Q = node_names


                global first_node
                first_node = node_names[0]

                i += 1
                continue

            #For the rest of the lines, connect edges to nodes given the input.
            line = input_file.readline()
            line_arr = line.split()
            graph.add_edge(line_arr[0], line_arr[1], line_arr[2])

            i += 1

    #The distance from each node to itself is 0
    for node in graph.nodes:
        graph.distances[(node,node)] = "0"

    return graph


def ls_routing(graph, src_node, outputfile):
    print("Link state routing results: ")
    dist = dict() #dist will be a dictionary of all the nodes in the graph and their distances from the source node
    prev = dict() #prev will be used to construct the least costly path by backtracking each node
    min_path = dict()

    global Q
    temp_Q = list()

    for node in Q:
        temp_Q.append(node)


    dist[src_node] = 0 #Distance from intitial node to initial node is 0
    prev[src_node] = None


    while temp_Q:

        #The source node will be selected first, it's distance from itself is 0
        u = None
        for node in temp_Q:
            if node in dist:
                if u is None:
                    u = node
                elif dist[node] < dist[u]:
                    u = node

        temp_Q.remove(u)

        #For each node in the network, compute the shortest path to it from the source node
        for edge in graph.edges[u]:

            alt = dist[u] + int(graph.distances[(u, edge)])

            if edge not in dist:
                dist[edge] = math.inf

            if alt < dist[edge]:
                dist[edge] = alt
                prev[edge] = u

    #Construct the paths for each node for the output file by backtracking with prev
    for node in Q:
        temp_Q.append(node)
    temp_Q.remove(src_node)

    for node in temp_Q:
        curr_node = node
        min_path[curr_node] = [curr_node]

        while prev[curr_node] != None:
            if prev[curr_node] not in min_path[node]:
                min_path[node].append(prev[curr_node])
            curr_node = prev[curr_node]

    for node in temp_Q:
        min_path[node] = list(reversed(min_path[node]))

    #Write our results to the output file
    with open(outputfile, "w") as outputfile:
        for node in temp_Q:
            outputfile.write(str(node) + ": ")
            print(str(node) + ": ", end = '')
            for edge in min_path[node]:
                outputfile.write(str(edge))
                print(str(edge), end = '')

                if edge == min_path[node][-1]:
                    outputfile.write(" "+ str(dist[node]))
                    print(" "+ str(dist[node]), end = '')
                    outputfile.write("\n")
                    print("\n", end = '')
                    continue

                outputfile.write("-")
                print("-", end = '')



def dv_routing(graph, src_node, outputfile):

    print("Distance vector routing results: ")
    dist = dict()
    prev = dict()
    global Q
    temp_Q = list()

    iterations = 0

    for node in Q:
        temp_Q.append(node)

    #Initialize the distances from the source node to each node in the network to infinity
    for node in Q:
        dist[node] = math.inf
    #Initialize the distance from the source node to itself to 0
    dist[src_node] = 0

    #Main part of the algorithm
    for i in range(0,len(graph.nodes)):
        for node in graph.nodes:
            for edge in graph.edges[node]:
                dist[edge] = min(dist[edge], dist[node] + int(graph.distances[(node,edge)]))

        iterations += 1



    #Initialize a table with all 0s
    table = []
    for i in range(0, len(graph.nodes) +1):
        table.append([])
        for j in range(0, len(graph.nodes)+1):
            table[i].append("0")


    #Fill in the first row and first column of the table
    for row in table:
        for val in row:

            if table.index(row) == 0 and row.index(val) == 0:
                table[table.index(row)][row.index(val)] = " "

            elif table.index(row) == 0:
                for node in temp_Q:
                    if temp_Q.index(node)+1 == row.index(val):
                        table[table.index(row)][row.index(val)] = node

            if table.index(row) > 0 and row.index(val) == 0:
                for node in temp_Q:
                    if temp_Q.index(node) + 1 == table.index(row):
                        table[table.index(row)][row.index(val)] = node


    #Fill in the rest of the table with distance values
    for row in table:
        for val in row:

            for node in temp_Q:
                if table.index(row) > 0:
                    if table[table.index(row)][row.index(val)] == node:
                        for i in range(1, len(graph.nodes)+1):

                            table[table.index(row)][row.index(val)+i] = graph.distances[(node, table[0][i])]
    i = 0

    #Print our results to system.out
    print("\t\tCost to\n")
    for row in table:
        if i == 1:
            print("From\t"+str(row)+"\n")
        else:
            print("\t\t"+str(row)+"\n")
        i +=1
    print("Number of rounds: ",iterations)

    #Write our results to the output file
    with open(outputfile, "w") as outputfile:
        outputfile.write("\t")
        outputfile.write("Cost to")
        outputfile.write("\n\n")
        i = 0
        for row in table:
            if i == 1:
                outputfile.write("From\t" + str(row))
                outputfile.write("\n")
            else:
                outputfile.write("\t" +str(row))
                outputfile.write("\n")
            i +=1
        outputfile.write("\n")
        outputfile.write("Number of rounds: "+str(iterations))


ls_routing(constructGraph(), first_node, "LS_output.txt")
print("\n")


dv_routing(constructGraph(), first_node, "DV_output.txt")



