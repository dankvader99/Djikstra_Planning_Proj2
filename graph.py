import cv2
import numpy as np


class Graph:
    
    action_set = [(( 1, 0), 1), (( 1, 1), 1.4),
                  (( 0, 1), 1), ((-1, 1), 1.4),
                  ((-1, 0), 1), ((-1,-1), 1.4),
                  (( 0,-1), 1), (( 1,-1), 1.4),]
    
    def __init__(self):
        # size of the map
        self.size = (400, 250)
        self.final_cost = np.full(self.size, np.inf)
        self.parent = np.full((*self.size, 2), -1)
        
        self.create_map()
    
    def create_map(self):

        x, y  = np.indices((400, 250))
            
        s1 = y-(0.316*x)-180.26
        s2 = y+(1.23*x)-218.19
        s3 = y+(3.2*x)-457
        s4 = y-(0.857*x)-102.135
        s5 = y+(0.1136*x)-189.09

        C = ((y -185)**2) + ((x-300)**2) - (40+5)**2  
        
        h1 = (y-5) - 0.577*(x+5) - 24.97
        h2 = (y-5) + 0.577*(x-5) - 255.82
        h3 = (x-6.5) - 235 
        h6 = (x+6.5) - 165 
        h5 = (y+5) + 0.577*(x+5) - 175 
        h4 = (y+5) - 0.577*(x-5) + 55.82 

        # print(h1.shape)

        self.map = ((h1 < 0) & (h2<0) & (h3<0) & (h4>0) & (h5>0) & (h6>0)) | (C<=0)  | ((s1<0) & (s5>0) & (s4>0)) | ((s2>0) & (s5<0) & (s3<0))
        self.map[:6, :] = 1; self.map[:, -6:] = 1
        self.map[:, :6] = 1; self.map[-6:, :] = 1


            
    def is_free(self, pos):
        # inside the map size
        if pos[0] < 0 or pos[1] < 0: 
            return False 
        if pos[0] >= self.size[0] or pos[1] >= self.size[1]: 
            return False 
        # and node is not closed or obstacle
        return self.map[pos] == 0 and self.final_cost[pos] == np.inf
    
    
    def do_action(self, pos, action):
        # get the direction to move and cost of the action
        move, move_cost = action
        # add the action step to node position to get new position
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        # add the cost of the action to get new cost
        new_cost = self.final_cost[pos] + move_cost
        return new_pos, new_cost
    
    
    def get_mapimage(self):
        img = np.full(self.size, 255, np.uint8)
        obs = np.where(self.map == 1)
        img[obs] = 50
        img = cv2.flip(cv2.transpose(img), 0)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img
        

    
if __name__ == '__main__':
    
    map = Graph()

    img = map.get_mapimage()
    
    cv2.imshow('test_map', img)
    cv2.waitKey(0)
    
