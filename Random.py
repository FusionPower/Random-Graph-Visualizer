# -*- coding: utf-8 -*-

import pygame
import random
import numpy as np

def raiz(nodo,p):
    if p[nodo]!=-1:
        return raiz(p[nodo],p)
    return nodo

def juntar(u,v,p):
    p[raiz(u,p)]=raiz(v,p)
 
def find_parent(max_hijos,index):
    if index%max_hijos==1:
        return index//max_hijos
    else:
        return int(np.ceil(index/max_hijos))
    
def arbol_aleatorio(max_hijos,max_altura,max_nodes):
    
    tree={}
    tree[1]=1
    max_nodes-=1
    max_index=0
    for i in range(max_altura+1):
        max_index+=max_hijos**i
    
    for i in range(max_nodes):
        node=random.randint(2,max_index)
        tree[node]=1
    
    l=sorted(list(tree.keys())[1:])
    for node in l:
        index=node
        tree.pop(index)
        while  find_parent(max_hijos,index) not in tree:
            index=find_parent(max_hijos,index)
        tree[index]=1
    
    l=list(tree.keys())
    l.sort(reverse=True)
    
    node_id={}
    start=0
    for i in reversed(l):
        node_id[i]=start
        start+=1
    

    edj=[]
    adj=[[] for i in range(start)]
    
    for v in l:
        if v==1:
            continue
        u=find_parent(max_hijos,v)
        
        u_i=node_id[u]
        v_i=node_id[v]
        
        edj.append([u_i,v_i])
        
        adj[u_i].append(v_i)
        adj[v_i].append(u_i)
    
    return adj,edj
    
def grafo_conexo_aleatorio(nodes,max_edges):
    if nodes<2:
        print()
        raise Exception("Please input more than 1 node")
        return -1
    if max_edges<nodes-1:
        print()
        raise Exception ("Edges must be >= nodes-1")
        return -2
    
    node_population=[i for i in range(nodes)]        
    adj=[[] for i in range(nodes)]
    edj=[]
    
    p=[-1]*nodes
    components=nodes
    
    linked={k:{} for k in range(nodes)}
    
    
    while components<=max_edges:
        s=random.sample(node_population,2)
        u=min(s)
        v=max(s)
        max_edges-=1
            
        if not linked[u].get(v,0):
            linked[u][v]=1
            adj[u].append(v)
            adj[v].append(u)
            edj.append([u,v])
            if raiz(u,p)!=raiz(v,p):
                juntar(u,v,p)
                components-=1
        
    

    raices=[]
    for i,v in enumerate(p):
        if v==-1:
            raices.append(i)
    
    for i in range(1,len(raices)):
        u=raices[i-1]
        v=raices[i]
        adj[u].append(v)
        adj[v].append(u)
        edj.append([u,v])
        
    return adj,edj
        

def erdos_renyi(n,p,w=1):
    
    
    adj=[[] for i in range(n)]
    edj=[]
    
    
    for i in range(n):
        for j in range(i+1,n):
            if random.random()<p:
                adj[i].append(j)
                adj[j].append(w)
                edj.append([i,j])
        
    return adj,edj

def erdos_renyi_edges(n,m,w=1):
    
    adj=[[] for i in range(n)]    
    all_edges=[[u,v] for u in range(n) for v in range(u+1,n)]
    
    edj=random.sample(all_edges,m)
    
    for e in edj:
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    
    return adj,edj
        
#################
####parameters###
#################


max_hijos=10
max_altura=5
max_nodes=10
max_edges=10
n=10
m=5
p=0.5


width=700
height=500


pygame.init()
window = pygame.display.set_mode((width, height))
window.fill((0, 0, 0))


mst_edge=(125,255,125)
node_color=(255, 0, 0)
red=(255, 0, 0)
white=(255,255,255)



edge_color=white
node_radius=10

class Edge:
    def __init__(self, node1, node2,weight=0,color=white):
        self.node1=node1
        self.node2=node2
        self.weight=weight
        self.color=color
    def pos1(self):
        return self.node1.pos
    def pos2(self):
        return self.node2.pos


class Node:
    def __init__(self, x, y, color, radius):
        self.pos = (x, y)
        self.x_boundary = (x - radius, x + radius)
        self.y_boundary = (y - radius, y + radius)
        self.color = color
        self.radius = radius
        self.edges=[]

    def recalc_boundary(self):
        self.x_boundary = (
            self.pos[0] - self.radius, self.pos[0] + self.radius
        )
        self.y_boundary = (
            self.pos[1] - self.radius, self.pos[1] + self.radius
        )
    def add_edge(self):
        
        return
        
def mouse_in_node():
    pos = pygame.mouse.get_pos()
    selected_node=None
    index=None
    for i,node in enumerate(nodes):
        if (within(pos[0], *node.x_boundary) and within(pos[1], *node.y_boundary)):
            selected_node=node
            index=i
    return selected_node,index





def generate_random_graph(adj,edj):
    nodes = []
    for i in range(len(adj)):
        x=random.randint(0,width)
        y=random.randint(0,height)
        
        nodes.append(Node(x,y,node_color,node_radius))

    for u,v in edj:
        
        u,v=min(u,v),max(u,v)
        
        new_edge=Edge(nodes[u],nodes[v])
        nodes[u].edges.append(new_edge)
        nodes[v].edges.append(new_edge)
    return adj,edj,nodes
    

nodes=[]
within = lambda x, low, high: low <= x <= high


selected = False
i=-1
selected_node=None

last_pos=None
drawing_edge=False


while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not selected_node and event.button == 1:
            pos = pygame.mouse.get_pos()
            selected_node,index=mouse_in_node()
                        
            if not selected_node:
                nodes.append(Node(pos[0], pos[1], red, 10))
            
        elif event.type==pygame.KEYDOWN:
            if event.key== pygame.K_LSHIFT:
                pos = pygame.mouse.get_pos()                
                node1,index=mouse_in_node()
                if node1:
                    last_pos=pos
                        
            
            if event.key==pygame.K_e:
                adj,edj=erdos_renyi(n,p)
                adj,edj,nodes=generate_random_graph(adj,edj)
            if event.key==pygame.K_m:
                adj,edj=erdos_renyi_edges(n,m)
                adj,edj,nodes=generate_random_graph(adj,edj)
            if event.key==pygame.K_c:
                adj,edj=grafo_conexo_aleatorio(n,max_edges)
                adj,edj,nodes=generate_random_graph(adj,edj)
            if event.key==pygame.K_a:
                
                adj,edj=arbol_aleatorio(max_hijos,max_altura,max_nodes)
                adj,edj,nodes=generate_random_graph(adj,edj)
            
                    
        elif event.type==pygame.MOUSEMOTION and last_pos:
            current_pos = pygame.mouse.get_pos()                
            drawing_edge=True

        elif event.type==pygame.KEYUP and drawing_edge:
            node2,index=mouse_in_node()
            if node1 and node2:
                new_edge=Edge(node1,node2)
                node1.edges.append(new_edge)
                node2.edges.append(new_edge)
            last_pos=None
            drawing_edge=False
            
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_node=None
            
        
            
    if selected_node:
        selected_node.pos = pygame.mouse.get_pos()
        selected_node.recalc_boundary()
        
    window.fill((0, 0, 0))
    if drawing_edge:
        pygame.draw.line(window, red, last_pos, current_pos, 1)

    for i,node in enumerate(nodes):
        pygame.draw.circle(
            window, node.color,
            node.pos,
            node.radius
        )
        for e,edge in enumerate(node.edges):
            pygame.draw.line(window, edge.color, edge.pos1(), edge.pos2(), 1)
    
    
    pygame.display.update()
