import random
import pickle

class Agent(object):
    
    NAME = "default_agent"
    
    def __init__(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None):
        """ Each agent is initialized at the beginning of each game.
            The first agent (id==0) can use this to set up global variables.
            Note that the properties pertaining to the game field might not be
            given for each game.
        """
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)
        
        # Read the binary blob, we're not using it though
        if blob is not None:
            print "Agent %s received binary blob of %s" % (
               self.callsign, type(pickle.loads(blob.read())))
            # Reset the file so other agents can read it.
            blob.seek(0) 
        
        # Recommended way to share variables between agents.
        if id == 0:
            self.all_agents = self.__class__.all_agents = []
        self.all_agents.append(self)
        
        #assuming the agent can move backward.
        #25,50
        #if(blob == None):
        ##self.stateActionValues = [[[[9.0 for move_y in range(0,9)] for move_x in range(0,9)] for y in range(0,27)]for x in range(0,49)]
        #else:
        self.stateActionValues = pickle.load(blob)
        #self.stateActionValues = tstateActionValues pickle.load(open("stateActionValues.p","wb"))
        self.action_taken = (0,0)
        self.old_state = (0,0)
        self.current_state  = (0,0)
        self.first_run = True
        
        #q learning variables:
        self.LR = 0.5
        self.DISCOUNT = 0.9
        
        #self.stateActionValues = pickle.load(open("stateActionValues.p","wb"))
        #pickle.dump(self.stateActionValues, open("stateActionValues.p","wb"))
        
        
    def observe(self, observation):
        """ Each agent is passed an observation using this function,
            before being asked for an action. You can store either
            the observation object or its properties to use them
            to determine your action. Note that the observation object
            is modified in place.
        """
        self.observation = observation
        self.selected = observation.selected
        if observation.selected:
            print observation
            
    def get_max_action(self,pos_x,pos_y):
        max_val = -10000
        x = 0
        y = 0
        #pos_x = self.current_state[0]
        #pos_y = self.current_state[1]
        '''
        print("for max values",self.current_state,pos_x,pos_y)
        for l in self.stateActionValues[self.current_state[0]][self.current_state[1]]:
                print(l)
        print("ACTIONMATRIX")
        '''
        for x_ in range(0,9):
            for y_ in range(0,9):
                if((x_ - 4)*10 + pos_x * 10 > 0 and (x_-4)*10 + pos_x * 10 < 496 and (y_ - 4)*10 + pos_y * 10 > 0 and (y_-4)*10 + pos_y * 10 < 272):
                    #if(x_-4 + pos_x > 0  and x_-4 + pos_x < 50 and y_-4 + pos_y > 0 and y_-4 + pos_y < 25):
                    if(self.stateActionValues[pos_x][pos_y][x_][y_] > max_val):
                        max_val = self.stateActionValues[pos_x][pos_y][x_][y_]
                        x = x_
                        y = y_
        #print("max at ",x,y,max_val)
        return([x,y,max_val])
    
    def action(self):
        """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """
        

        
        self.current_state = (int(self.observation.loc[0]/10 ), int(self.observation.loc[1]/10))
        if(self.first_run):
            self.old_state = self.current_state

            
        if(self.first_run == False):#observe reward
            reward = 0
            
            
            cps1_loc = self.observation.cps[0][0:2]
            cps2_loc = self.observation.cps[1][0:2]
            loc = self.observation.loc
            
            if not self.current_state == self.old_state:
                if(point_dist(loc, cps1_loc) < self.settings.tilesize):
                    reward += 100
                if(point_dist(loc, cps2_loc) < self.settings.tilesize):
                    reward += 100
                
                
    
            
            #decide which action to take
            x = int(self.observation.loc[0]/10)
            y = int(self.observation.loc[1]/10)

            ret  = self.get_max_action(x,y)
            x = ret[0]
            y = ret[1]
            #print("current_action:",x,y)
            #print("current_state",self.current_state[0],self.current_state[1])
            #learning:
            future_reward = self.stateActionValues[self.current_state[0] ] [ self.current_state[1]][x][y]
            old_value = self.stateActionValues[self.old_state[0] ] [ self.old_state[1]][self.action_taken[0]][self.action_taken[1]]
            self.stateActionValues[self.old_state[0] ] [ self.old_state[1]][self.action_taken[0]][self.action_taken[1]] += self.LR * (reward + self.DISCOUNT * future_reward - old_value  )
            #print("real values")
            for x_ in self.stateActionValues[self.current_state[0]][self.current_state[1]]:
                print(x_)
            
            #print(self.stateActionValues[self.current_state[0] ] [ self.current_state[1]][x][y])
            #if(self.old_state == self.current_state and not self.first_run):
            #    self.stateActionValues[self.current_state[0] ] [ self.current_state[1]][x][y] = -10.0 #WALL!
            
            #execute action decided on
            self.action_taken = (x,y)
            #convert to continuous space
            x = ret[0]-4
            y = ret[1]-4
            #print("direction:",x*10,y*10)
            
            self.goal = (x*10 + self.current_state[0] * 10 , y*10 + self.current_state[1] * 10 )
            if(not(self.goal[0] > 0 and self.goal[0] < 496 and self.goal[1]>0 and self.goal[1]< 272)):
                
                print("something went wrong with goal:",self.goal[0],self.goal[1])
                print("action:",self.action_taken)
                print("in:",self.current_state)
                self.goal = (24,120)
            #print(self.stateActionValues[self.old_state[0] ] [ self.old_state[1]][self.action_taken[0]][self.action_taken[1]])
            

            
        #convert goal to range and bearing
        turn = 0
        speed = 0
        shoot = False
        #take action
        #print("new goal:",self.goal)
        if(not self.goal == None):
            path = find_path(self.observation.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
            if path:
                dx = path[0][0] - self.observation.loc[0]
                dy = path[0][1] - self.observation.loc[1]
                turn = angle_fix(math.atan2(dy, dx) - self.observation.angle)
                if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                    shoot = False
                speed = (dx**2 + dy**2)**0.5
            else:
                turn = 0
                speed = 0
                
        self.old_state = self.current_state
        self.first_run = False
        return(turn,speed,shoot)
    
            
    def debug(self, surface):
        """ Allows the agents to draw on the game UI,
            Refer to the pygame reference to see how you can
            draw on a pygame.surface. The given surface is
            not cleared automatically. Additionally, this
            function will only be called when the renderer is
            active, and it will only be called for the active team.
        """
        import pygame
        # First agent clears the screen
        if self.id == 0:
            surface.fill((0,0,0,0))
        # Selected agents draw their info
        if self.selected:
            if self.goal is not None:
                pygame.draw.line(surface,(0,0,0),self.observation.loc, self.goal)
        p = [(24, 120), (24, 136),(24, 152)]
        #bot
        path1 = [(24, 152),(50,185),(195,218)]#[(24, 152),(57,185),(192,218)]
        #up
        path2 = [(24, 120),(50,90),(180,39)]#55,80,180,39
        
        p1 = path1[0]
        p2 = path1[1]
        p3 = path1[2]
        
        #self.draw_line(surface, p1,p2)
        #self.draw_line(surface,p2,p3)
        
        p1 = path2[0]
        p2 = path2[1]
        p3 = path2[2]
        #self.draw_line(surface,p1,p2)
        #self.draw_line(surface,p2,p3)
    def draw_line(self,surface,from_,to_):
        import pygame
        pygame.draw.line(surface,(0,0,0),from_,to_)
        
        
    def draw_circle(self,loc,radius,color,surface):
        self.draw_dot((loc[0]+radius,loc[1]),surface,color)
        self.draw_dot((loc[0],loc[1]+radius),surface,color)
        self.draw_dot((loc[0]-radius,loc[1]),surface,color)
        self.draw_dot((loc[0],loc[1]-radius),surface,color)
        #for x in range(loc[0]-41,loc[0]+41):
        #    for y in range(loc[1]-41,loc[1]+41):
        
        #for x in range(loc[0]-)
    def draw_path(self,path,surface):
        for point in path:
            for x in range(point[0]-2,point[0]+2):
                for y in range(point[1]-2,point[1]+2):
                    surface.set_at((x,y),(250,0,0,255))
                    
    def draw_dot(self,center,surface,color):
        for x in range(center[0]-2,center[0]+2):
            for y in range(center[1]-2,center[1]+2):
                surface.set_at((x,y),color)
                
    def finalize(self, interrupted=False):
        """ This function is called after the game ends, 
            either due to time/score limits, or due to an
            interrupt (CTRL+C) by the user. Use it to
            store any learned variables and write logs/reports.
        """
        print("FINALIZING")
        #pickle.dump(self.stateActionValues, open("stateActionValues.p","wb"))
        print("written pickle")
        pass
        
