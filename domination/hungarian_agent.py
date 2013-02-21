from munkres import Munkres, print_matrix



class Agent(object):
    
    '''
    agent with id==1: goes from one ammo to the other
    agent with id==0: goes from south cp to south camping and vice versa
    agent with id==2: goes from north cp to north camping and vice versa
    '''
    NAME = "default_agent"
    
    '''
    finds the length of the path
    '''
    def get_path_length(self,loc,path):
        current_pos = loc
        length = 0
        for point in path:
            dx = point[0] - current_pos[0]
            dy = point[1] - current_pos[1]
            length += sqrt(dx*dx + dy*dy)
            current_pos = point
            
        return(length)
    
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
        
        #initialize matrix for hungarian algorithm
        #self.costMatrix=[[0.0]*3]*3
        self.costMatrix = [[0 for i in range(4)] for j in range(3)]
        
        #role for agent:
        '''
        x-Ammo
        O-controlpoint
        
          5-O-4
          |   |
         0x  3x
          |   |
          1-0-2
        '''
        self.role = 0
        
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
        
        
        #assign init roles:
        if(self.id == 0):
            #self.role = 1
            self.role = 1
        if(self.id == 1):
            #self.role = 3
            self.role = 3
        if(self.id == 2):
            #self.role = 4
            self.role = 4
            
    
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
                    
    def action(self):
        """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """
        turn = 0
        speed = 0
        shoot = False

        
        obs = self.observation  
        #print(self.role)
        
        
        
        #set goals according to roles:
        '''
        if(self.role == 0): #left ammo (152,136)
            self.goal = (152,136)#(152,151)
            
            #up
            if(point_dist((152,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,111)
            #down
            if(point_dist((152,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,151)
            
        if(self.role == 3): #right ammo (312,136)
            self.goal = (312,136)#(312,151)
            
            #up
            if(point_dist((312,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,111)
            #down
            if(point_dist((312,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,151)
            
        if(self.role == 1): #bot cp
            self.goal = (248, 216)
        if(self.role == 4):#top cp
            self.goal = (220, 56)
            
        if(self.role == 2): #go to right ammo
            self.goal = (312,136)
        if(self.role == 5): #go to left ammo
            self.goal = (152,136)
            
        if(self.role == 6): #camping south
            self.goal = (320,250)
        if(self.role == 7): #camping north
            self.goal = (150,40)
            #####
            #####
        #check if there:
        '''
        
        

        # Check if agent reached goal.
        #if self.goal is not None and point_dist(self.goal, obs.loc) < self.settings.tilesize:
        #    self.goal = None
            
        # Walk to ammo
        #ammopacks = filter(lambda x: x[2] == "Ammo", obs.objects)
        #if ammopacks:
        #    self.goal = ammopacks[0][0:2]
            
        # Drive to where the user clicked
        # Clicked is a list of tuples of (x, y, shift_down, is_selected)
        if self.selected and self.observation.clicked:
            self.goal = self.observation.clicked[0][0:2]
        
        # Walk to random CP
        #if self.goal is None:
        #    self.goal = obs.cps[random.randint(0,len(obs.cps)-1)][0:2]
        
        # if see enemy Shoot
        shoot = False
        if (obs.ammo > 0 and obs.foes and point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True
        #else define the goal of the agent
        #check if we dont own any cp (cps: (x,y,flag))
        elif ( obs.cps[1][2] != self.team and obs.cps[0][2] != self.team):
            #flags:
            #0 -> red
            #1 -> blue
            #2 -> neutral
            #print obs.cps[1][2]  
            #print self.team
            
            
            #path for bottom cp for agent 0
           # self.path1=find_path(self.all_agents[0].observation.loc, (248, 216), self.mesh, self.grid, self.settings.tilesize)
            #path for top cp for agent 0
            x=0;
            for id in self.all_agents:
                path1=find_path(id.observation.loc, (220, 56), self.mesh, self.grid, self.settings.tilesize)
                path2=find_path(id.observation.loc, (248, 216), self.mesh, self.grid, self.settings.tilesize)
                path3=find_path(id.observation.loc, (152,136), self.mesh, self.grid, self.settings.tilesize)
                path4=find_path(id.observation.loc, (312,136), self.mesh, self.grid, self.settings.tilesize)

                self.costMatrix [x][0] = self.get_path_length(id.observation.loc,path1)
                self.costMatrix [x][1] = self.get_path_length(id.observation.loc,path2)
                self.costMatrix [x][2] = self.get_path_length(id.observation.loc,path3)
                self.costMatrix [x][3] = self.get_path_length(id.observation.loc,path4)

                x=x+1
            print self.costMatrix
            ##print self.costMatrix[1][1]
            
            m = Munkres()
            indexes = m.compute(self.costMatrix)
            #print_matrix(self.costMatrix, msg='Lowest cost through this matrix:')
            total = 0
            for row, column in indexes:
                value = self.costMatrix[row][column]
                total += value
                print '(%d, %d) -> %d' % (row, column, value)
                if (column==0):
                    self.all_agents[row].goal= (220, 56)
                elif (column==1):
                    self.all_agents[row].goal= (248, 216)
                elif (column==2):
                    self.all_agents[row].goal= (152,136)
                elif (column==3):
                    self.all_agents[row].goal= (312,136)
                #print 'goal : ', self.all_agents[row].goal
                #print 'agent : ', row
            print 'total cost: %d' % total

        #turn = math.pi/4
        speed = 0
        if (not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            #goto goal!
        
            path = find_path(obs.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
            #print(self.id,"i keep movin movin movin")
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            if(not shoot):
                speed = (dx**2 + dy**2)**0.5
         
            
            
        else: #reached whatever goal it was:
            #just circle
            a=1
        return (turn,speed,shoot)
        
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
        
    def finalize(self, interrupted=False):
        """ This function is called after the game ends, 
            either due to time/score limits, or due to an
            interrupt (CTRL+C) by the user. Use it to
            store any learned variables and write logs/reports.
        """
        pass
        

