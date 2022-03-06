import cv2
import numpy as np
from graph import Graph
       
       
def dijsktra_search(graph, start_node, goal_node):
    ''' Search for a path from start to given goal position
    '''
    explored = [start_node]  
    cost_dict = {start_node: 0}
    # Run Dijkstra Algorithm
    while len(cost_dict):
        curr_node = min(cost_dict, key = cost_dict.get)
        graph.final_cost[curr_node] = cost_dict.pop(curr_node)
        # if the new_node is goal backtrack and return path
        if curr_node == goal_node:
            return backtrack(graph, curr_node), explored
        # get all children of the current node
        for action in graph.action_set:
            child_node, new_cost = graph.do_action(curr_node, action)
            # if the new position is not free, skip the below steps
            if not graph.is_free(child_node): continue
            # update cost and modify cost_dict
            if new_cost < cost_dict.get(child_node, np.inf):
                graph.parent[child_node] = curr_node
                cost_dict[child_node] = new_cost 
                explored.append(child_node)
    # return None if no path is found.
    return None, None

def backtrack(graph, node):
    path = []
    while graph.parent[node][0] != -1:
        path.append(node)
        node = tuple(graph.parent[node])
    path.reverse()
    return path
    

def visualize(path, explored):
    ''' Visualise the exploration and the recently found path
    '''
    img = graph.get_mapimage()
    h, w, _ = img.shape
    out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 60.0, (w, h))
    
    for i in range(len(explored)):
        pos = (249 - explored[i][1], explored[i][0])
        img[pos] = [0, 255, 0]
        if i%100 == 0:
            out.write(img)
            cv2.imshow('hi', img)
            cv2.waitKey(1)
    for pos in path:
        pos = (249 - pos[1], pos[0])
        img[pos] = [0, 0, 255]
    for i in range(50): 
        out.write(img)
    out.release()
    cv2.imshow('hi', img)
    cv2.waitKey(0)
    

            

# when running as main 
if __name__ == '__main__':
    #give start and goal states\

    graph = Graph()

    start = input("Enter start coordinates: ")
    start_x, start_y = start.split()
    start = int(start_x), int(start_y)
    if not graph.is_free(start):
        print("In valid start node or in Obstacle space")
        exit(-1)
    
    goal = input("Enter goal coordinates: ")
    goal_x, goal_y = goal.split()
    goal= int(goal_x), int(goal_y)

    if not graph.is_free(goal):
        print("In valid goal node or in Obstacle space")
        exit(-1)


    path, explored = dijsktra_search(graph, start, goal)
    
    img = graph.get_mapimage()

    visualize(path, explored)
    # print('\nThe sequence of actions from given start to goal is:')
    # print(solution, '\n')