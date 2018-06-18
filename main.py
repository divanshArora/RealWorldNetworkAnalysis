#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 17:18:16 2018
@author: divansh
DATASET: http://networkrepository.com/ca-netscience.php
"""
import io
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import queue


def plot_dict(title, degdict):
    lx = sorted(degdict.items()) # sorted by key, return a list of tuples
    x, y = zip(*lx)
    plt.plot(x,y)
    plt.title(title)
    plt.show()
    

def bfs(src, graph, V):
    visited = [0]*(V+1)
    q = queue.Queue()
    tim = 0
    q.put((src,tim))
    num = 0
    visited[src]=1
    while(not q.empty()):
        u = q.get()
#        visited[u[0]]=1
        num+=u[1]
        for i in graph[u[0]]:
            if(visited[i]==0):
                q.put((i,u[1]+1))
                visited[i]=1                
#    for i in visited:
#        if(i==1):
#            den+=1
    return num/V
        

def num_path(curr, parent, num_paths, dict_node, src):
    #print("curr = ",curr, "parent = ",parent, "num pth= ",num_paths, "src = ",src)
    if(curr==src):
        #print("curr is src")
        return 1
    tp = 0
    for p in parent[curr]:
#        if(p in dict_node):
#            dict_node[p]+=1
#        elif(p not in dict_node):
#            dict_node[p]=1
        if(curr in dict_node):
            dict_node[curr]+=1
        else:
            dict_node[curr]=1
        sm =num_path(p,parent,num_paths,dict_node,src)
        #print("sm = ",sm)
        tp+=sm
    #print("tp = ",tp)
    return tp

def bfs_between(src, graph, V,ret):
    visited = [0]*(V+1)
    parent = defaultdict(list)
    dist =  [0]*(V+1)
    q = queue.Queue()
    tim = 0
    q.put((src,tim))
    num = 0
    parent[src].append(-1);
    ans_dict = {}
    visited[src]=1
    while(not q.empty()):
        u = q.get()
        #print("current node = ",u)
#        visited[u[0]]=1
        num+=u[1]
        for i in graph[u[0]]:
            #print("dist before loop",dist)
            if(visited[i]==0):
                #print(i," was not visited")
                q.put((i,u[1]+1))
                dist[i] = u[1]+1
                visited[i]=1
                parent[i].append(u[0])
                #print("parent of ",i, " is ",u[0])
                #print("dist = ",dist)
            elif(visited[i]==1 and dist[i]==u[1]+1):
                parent[i].append(u[0])
                #print("parent of ",i, " is ",u[0], "but it was visited")
    #print("BFS COMPLETED---------------------------")
#    ret= {}
    for i in graph.keys():
        if(visited[i]==1 and i!=src):
            td = {}
            #print("Going into num path for ",i)
            ans_dict[i] = num_path(i,parent,0,td,src)
            num_paths_from_i_to_src = ans_dict[i]
            for k in td.keys():
                if(k!=src and k!=i):
                    num_times_k_appears_in_these_paths = td[k]
                    #print("Number of times ",k, " appers in path from ",i," to ",src," is ",num_times_k_appears_in_these_paths)
                    #print("num of paths from i to src = ",num_paths_from_i_to_src)
                    if(k not in ret):
                        ret[k] = num_times_k_appears_in_these_paths/num_paths_from_i_to_src
                    else:
                        ret[k] += num_times_k_appears_in_these_paths/num_paths_from_i_to_src
    return (ret,ans_dict)

if __name__=='__main__':
    edgeset = set()
    graph = defaultdict(list)
    V = 0
    E = 0
    with io.open('ca-netscience.mtx','r') as file:
#    with io.open('test.txt','r') as file:
        l= 0
        for line in file:
            if(l==0):
                ls = line.split();
                V= int(ls[0])
                E =int(ls[1])
                l+=1
            else:
                ls = line.split();
                u = int(ls[0])
                v = int(ls[1])
                edgeset.add((u,v))
                edgeset.add((v,u))
                graph[u].append(v)
                graph[v].append(u)
        degdict = {}
        for k in graph.keys():
            d = 2*(len(graph[k]))
            if d not in degdict:
                degdict[d]=1
            else:
                degdict[d]+=1
        plot_dict("Degree vs Number of nodes- degree distribution",degdict)
        clustering_coefficient={}
        for node in graph.keys():
            neighbour_list = graph[node]
            num = 0
            for i in neighbour_list:
                for j in neighbour_list:
                    t = (i,j)
                    if(t in edgeset):
                        num+=1
            l= len(neighbour_list)
            if(l>1):
                clustering_coefficient[node] = ((num))/(l*(l-1))
        plot_dict("clustering coefficient",clustering_coefficient)
        closeness_centrality= {}
        for src in graph.keys():
            closeness_centrality[src] = bfs(src,graph, V)
        plot_dict("Closeness centrality- lower is better", closeness_centrality)
        ret = {}
        for node in graph.keys():
            #print("_+++==================================================================")
            #print("running with src as",node)
            ret,ans_dict = bfs_between(node,graph,V,ret)
#        ret,ans_dict = bfs_between(2,graph,V,ret)
        x = list(range(1,V+1))
        y = [0]*V
        for k in ret:
            ret[k] = ret[k]/2
            y[k] = ret[k]
        plt.plot(x,y)
        plt.title("betweeness centrality - in var ret")
        plt.show()
        
        print("COMPLETED")
                
                
                
                
    