### Name: Kevin San Gabriel
### Student ID: 301342241
### CMPT 371
### Project 1

import random
import os
import math

class node:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.key = []
        self.succ_table = None

input_file_name = input()
def chord_dht(inputfile, outputfile):

    S = None
    N = None
    M = None
    hashed_ids = list()
    hashed_ids_string = list()
    hashed_keys = list()
    hashed_keys_string = list()
    end = list()
    end_string = list()
    node_list = list()

    with open(inputfile, "r") as input_file:

        S = int(input_file.readline())
        N = int(input_file.readline())
        M = int(input_file.readline())

        hashed_ids_string = input_file.readline().split(',')
        for id in hashed_ids_string:
            #hashed_ids.insert(int(id),int(id))
            hashed_ids.append(int(id))

        hashed_keys_string = input_file.readline().split(',')
        for key in hashed_keys_string:
            #hashed_keys.insert(int(key),int(key))
            hashed_keys.append(int(key))

        end_string = input_file.readline().split(',')
        for end_value in end_string:
            end.append(int(end_value))

        temp_hashed_ids = hashed_ids

        #Assign a node id to a node
        while len(temp_hashed_ids) != 0:
            node_id = random.sample(temp_hashed_ids,1)[0]
            aNode = node(node_id)
            temp_hashed_ids.remove(node_id)
            node_list.append(aNode)

        temp_hashed_keys = hashed_keys.copy()
        while len(temp_hashed_keys) != 0:
            key = random.sample(temp_hashed_keys, 1)[0]
            min = 999999
            for node_item in node_list:

                difference = (node_item.peer_id - key) % S
                if abs(difference) < min:
                    min = abs(difference)

            for node_item in node_list:
                if node_item.peer_id == (key + min) % S:
                    node_item.key.append(key)


            temp_hashed_keys.remove(key)


        #Initialize successor table for each node
        for node_item in node_list:
            table = list()
            for i in range(0,M+1):
                table.append([])
            node_item.succ_table = table

        ring = [None] * int(S+1)

        for node_item in node_list:
            ring[node_item.peer_id] = node_item


        #Update successor table for each node
        for node_item in ring:
            if node_item != None:

                for i in range(0, round(math.log(S, 2))):

                    node_item.succ_table[i].append(i)
                    node_item.succ_table[i].append((node_item.peer_id + pow(2,i)) % int(S+1))

                    k = 1
                    while(1):
                        if ring[((node_item.peer_id + pow(2,i))) % int(S+1)] != None:
                            if ring[((node_item.peer_id + pow(2,i))) % int(S+1)].peer_id == (node_item.peer_id + pow(2, i)) % int(S + 1):
                                node_item.succ_table[i].append(ring[((node_item.peer_id + pow(2,i))) % int(S+1)].peer_id)
                                break

                        elif ring[((node_item.peer_id + pow(2,i))+k) % int(S+1)] != None:
                             node_item.succ_table[i].append(ring[((node_item.peer_id + pow(2,i))+k) % int(S+1)].peer_id)
                             break
                        k = k+1

        temp_hashed_keys = hashed_keys.copy()

        with open(outputfile, "w") as output_file:
            for key in temp_hashed_keys:
                for node_item in node_list:
                    if key in node_item.key:
                        output_file.write(str(node_item.peer_id) + "\n")
                        for row in node_item.succ_table:
                            if row:

                                for i in range(0, len(row)):
                                    if i == len(row) - 1:
                                        output_file.write(str(row[i]))
                                    else:
                                        output_file.write(str(row[i]) + " ")
                                """
                            
                                for item in row:
                                    output_file.write(str(item) + " ")
                                """
                                output_file.write("\n")







chord_dht(input_file_name,os.path.splitext(input_file_name)[0] + ".out")
