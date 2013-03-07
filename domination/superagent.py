import pickle
import os.path
from domination import core
from domination.libs import astar
from libs.munkres import Munkres, print_matrix

class Agent(object):

    NAME = "KyleReese"
    def __init__(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None,matchinfo=None):
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
        self.counter = 0
        self.AP = [(184,168), (312, 104)]
        #self.pathRTCP = [(50,90), (180,39), obs.cps[1][0:2]]
        #self.pathRBCP = [(50,185), (195,218), obs.cps[0][0:2]]
        self.policy = 0 #"defensive", "hungarian", "bigloop", "twinloops", "defensive hungarian"
        self.result = "W"
        self.memory = []
        #role for agent:
        '''
        x-Ammo
        O-controlpoint

          5-O-4
          |   |
         3x   0x
          |   |
          1-O-2
        '''
        self.role = 0
        
        
        #initialize super game memory
        #[games,wins,policy]
        self.gamwinpol = [0,0,0]
        '''
        if(os.path.exists("tmemory.p")):        
            self.gamwinpol = pickle.load(open("tmemory.p","rb"))
            print("man i read:", self.memory)
            #if (len(self.memory) >= 20):
            #    self.memory = self.memory[-20]
            #    #self.policy = self.memory[0][0]
            #    wins = zip(*self.memory)[1].count("W")
            #    if (wins < 10):
            #        self.policy = self.policy + 1
            self.policy = self.gamwinpol[2]
            
            if(self.gamwinpol[0]>= 20):
                if(self.gamwinpol[1] < 10):
                    self.policy = (self.policy + 1 )% 6
                    self.gamwinpol = [0,0,self.policy]
                else:
                    self.gamwinpol = [0,0,self.policy]
                    
            print ("policy:",self.policy)
            print ("policyfromfile:",self.gamwinpol[2])
            print ("wins:",self.gamwinpol[1])
            print("no_games: ",self.gamwinpol[0])

            #count = zip(*self.memory)[1].count("W")
            #count = count/3.4
            #print "count:",count
        '''
        # Read the binary blob, we're not using it though
        if blob is not None:
            # Reset the file so other agents can read it.
            try:    
                blob.seek(0)
                #print "Agent %s received binary blob of %s" % (
                #   self.callsign, type(pickle.loads(blob.read())))
                self.gamwinpol = pickle.loads(blob.read())
                print "Blob Read!"
            except:
                print "Blob read error: Make sure to have Read Access!"
  
            if( self.gamwinpol == [] ):
                self.gamwinpol = [0,0,0]
            self.policy = self.gamwinpol[2]
            
            if(self.gamwinpol[0]>= 20):
                if(self.gamwinpol[1] < 10):
                    self.policy = (self.policy + 1 )% 6
                    self.gamwinpol = [0,0,self.policy]
                else:
                    self.gamwinpol = [0,0,self.policy]
                    
            print ("policy:",self.policy)
            print ("policy from file:",self.gamwinpol[2])
            print ("wins:",self.gamwinpol[1])
            print("no_games: ",self.gamwinpol[0])
        



        #self.policy = 0        
        # Recommended way to share variables between agents.
        if id == 0:
            self.all_agents = self.__class__.all_agents = []
        self.all_agents.append(self)
        if(self.policy == 0): #defensive_agent
            self.init_defensive(id, team, settings, field_rects, field_grid, nav_mesh, blob)
        elif(self.policy == 1): #def_hung
            self.init_def_hung(id, team, settings, field_rects, field_grid, nav_mesh, blob)
        elif(self.policy == 2): #hung
            self.init_hung(id, team, settings, field_rects, field_grid, nav_mesh, blob)
        elif(self.policy == 3): #T-600
            self.init_t_600(id, team, settings, field_rects, field_grid, nav_mesh, blob)
        elif(self.policy == 4): #deterministic_agent2
            self.init_det_ag2(id, team, settings, field_rects, field_grid, nav_mesh, blob)
        elif(self.policy == 5): #agent.py
            self.init_agent(id, team, settings, field_rects, field_grid, nav_mesh, blob)
        
    def init_defensive(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None): 
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)


        #role for agent:
        '''
        x-Ammo
        O-controlpoint

          5-O-4
          |   |
         3x   0x
          |   |
          1-O-2
        '''
        self.role = 0








        #assign init roles:
        '''
        if (self.team==TEAM_BLUE):
            self.role=1
        else:
            self.role=4
        '''   
        if(self.id == 0):
            self.role = 4

        if(self.id == 1):
            if(self.team == TEAM_RED):          
                self.role = 4
            else:
                self.role = 1

        if(self.id == 2):
            #self.role = 4
            self.role = 1
            
    def init_def_hung(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None): 
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)
        
        #initialize matrix for hungarian algorithm
        #self.costMatrix=[[0.0]*3]*3
        self.costMatrix = [[0 for i in range(3)] for j in range(3)]
        self.costMatrix2 = [[0 for i in range(4)] for j in range(3)]
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
    
    def init_hung(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None): 
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

    def init_t_600(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None): 
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)


        #role for agent:
        '''
        x-Ammo
        O-controlpoint

          5-O-4
          |   |
         3x   0x
          |   |
          1-O-2
        '''
        self.role = 0








        #assign init roles:
        if(self.id == 0):
            #self.role = 1
            self.role = 1
        if(self.id == 1):
            #self.role = 3
            self.role = 5
        if(self.id == 2):
            #self.role = 4
            self.role = 4

    def init_det_ag2(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None): 
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)
        
        
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
            
    def init_agent(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None): 
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)
        



    
    def observe(self, observation):
        """ Each agent is passed an observation using this function,
            before being asked for an action. You can store either
            the observation object or its properties to use them
            to determine your action. Note that the observation object
            is modified in place.
        """
        if(self.policy == 0): #defensive_agent
            self.obs_defensive( observation)
        elif(self.policy == 1): #def_hung
            self.obs_def_hung( observation)
        elif(self.policy == 2): #hung
            self.obs_hung( observation)
        elif(self.policy == 3): #T-600
            self.obs_t_600( observation)
        elif(self.policy == 4): #deterministic_agent2
            self.obs_det_ag2( observation)
        elif(self.policy == 5): #agent.py
            self.obs_agent( observation)

    def obs_defensive(self, observation):
        self.observation = observation
        self.selected = observation.selected

        if observation.selected:
            print observation
            
    def obs_def_hung(self, observation):
        self.observation = observation
        #print observation
        self.selected = observation.selected
        
        if observation.selected:
            print observation
    def obs_hung(self,observation):
        self.observation = observation
        print observation
        self.selected = observation.selected
        
        if observation.selected:
            print observation
    def obs_t_600(self,observation):
        self.observation = observation
        self.selected = observation.selected

        if observation.selected:
            print observation
    def obs_det_ag2(self,observation):
        self.observation = observation
        self.selected = observation.selected
        
        if observation.selected:
            print observation
    def obs_agent(self,observation):
        self.observation = observation
        self.selected = observation.selected
        
        if observation.selected:
            print observation

    def action(self):
        turn = 0
        speed = 0
        shoot = 0
        print("POLICY",self.policy)
        if(self.policy == 0): #defensive_agent
            turn,speed,shoot = self.action_defensive( )
        elif(self.policy == 1): #def_hung
            turn,speed,shoot = self.action_def_hung( )
        elif(self.policy == 2): #hung
            turn,speed,shoot = self.action_hung( )
        elif(self.policy == 3): #T-600
            turn,speed,shoot = self.action_t_600( )
        elif(self.policy == 4): #deterministic_agent2
            turn,speed,shoot = self.action_det_ag2( )
        elif(self.policy == 5): #agent.py
            turn,speed,shoot = self.action_agent( )
            
        return (turn,speed,shoot)
    
    def action_defensive(self):
        turn = 0
        speed = 0
        shoot = False


        obs = self.observation
        #print(self.role)



        #set goals according to roles:

        if(self.role == 0): #left ammo
            self.goal = self.AP[0]
            '''
            #up
            if(point_dist((152,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,111)
            #down
            if(point_dist((152,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,151)
            '''
        if(self.role == 3): #right ammo self.AP[1]
            self.goal = self.AP[1]#(312,151)
            '''
            #up
            if(point_dist((312,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,111)
            #down
            if(point_dist((312,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,151)
            '''
        if(self.role == 1): #bot cp
            self.goal = obs.cps[0][0:2]
        if(self.role == 4):#top cp
            self.goal = obs.cps[1][0:2]

        if(self.role == 2): #go to right ammo
            self.goal = self.AP[1]
        if(self.role == 5): #go to left ammo
            self.goal = self.AP[0]

        #if(self.role == 6): #go to left ammo
            #self.goal = (320,250)
        #if(self.role == 7): #go to left ammo
            #self.goal = (150,136)
            #####
            #####
        #check if there:




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

        # Shoot enemies
        shoot = False
        if (obs.ammo > 0 and obs.foes and point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True



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
            '''if(self.role < 5 and self.role >= 0):
                self.role += 1
            else:
                self.role = 0
            '''
            if (self.role == 0): ##2,4
                self.role = 3

            elif (self.role == 1): ##2,4
                self.role = 1

            elif (self.role == 2): ##2,4
                self.role = 4

            elif (self.role == 3):
                self.role = 0

            elif (self.role == 4):
                self.role = 4

            elif (self.role == 5):
                self.role = 1

            '''
            if(self.role == 1 or self.role == 4):#reached the cp
                self.role += 1
            elif(self.role == 5):#clap with other agent
                for i in range(len(self.all_agents)):
                    if(self.all_agents[i].role == 0): #change others agants role !
                        self.all_agents[i].role = 1
                self.role = 0

            elif(self.role == 2): #clap with other agent
                for i in range(len(self.all_agents)):
                    if(self.all_agents[i].role == 3):
                        self.all_agents[i].role = 4
                        break
                self.role = 3
            '''
        '''
        if(self.id == 1 and not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        '''
        '''
        if(self.id == 2 and not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        '''

        #if(self.id = 0 and not obs.loc == self.goal):
        #    pass


        #if(self.id == 0):
        #    print(turn,speed,self.id)
        return (turn,speed,shoot)
    
    def get_path_length(self,loc,path):
        current_pos = loc
        length = 0
        for point in path:
            dx = point[0] - current_pos[0]
            dy = point[1] - current_pos[1]
            length += sqrt(dx*dx + dy*dy)
            current_pos = point
            
        return(length)
    
    
    
    
    def action_def_hung(self):
        turn = 0
        speed = 0
        shoot = False

        
        obs = self.observation  
        #print(self.role)
        
        
        
        #set goals according to roles
        
        

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
        elif (obs.ammo > 0 and obs.cps[1][2] == self.team and obs.cps[0][2] == self.team  ):
            self.goal = obs.cps[random.randint(0,len(obs.cps)-1)][0:2]
        #else define the goal of the agent
        elif (obs.cps[1][2] == self.team and obs.cps[0][2] == self.team ):
#        ( obs.cps[1][2] != self.team and obs.cps[0][2] != self.team ):   
            #flags:
            #0 -> red
            #1 -> blue
            #2 -> neutral
            #print obs.cps[1][2]  
            #print self.team      
            #path for bottom cp for agent 0
            #self.path1=find_path(self.all_agents[0].observation.loc, obs.cps[0][0:2], self.mesh, self.grid, self.settings.tilesize)
            #path for top cp for agent 0
            x=0;
            for id in self.all_agents:
                #top cp
                path1=find_path(id.observation.loc, obs.cps[1][0:2], self.mesh, self.grid, self.settings.tilesize)
                #bottom cp
                path2=find_path(id.observation.loc, obs.cps[0][0:2], self.mesh, self.grid, self.settings.tilesize)
                #left ammo
                path3=find_path(id.observation.loc, self.AP[0], self.mesh, self.grid, self.settings.tilesize)
                #right ammo
                path4=find_path(id.observation.loc, self.AP[1], self.mesh, self.grid, self.settings.tilesize)

                self.costMatrix2 [x][0] = 0.1*self.get_path_length(id.observation.loc,path1)
                self.costMatrix2 [x][1] = 0.1*self.get_path_length(id.observation.loc,path2)
                self.costMatrix2 [x][2] = 0.1*self.get_path_length(id.observation.loc,path3)
                self.costMatrix2 [x][3] = 0.1*self.get_path_length(id.observation.loc,path4)

                x=x+1
           # print self.costMatrix
            ##print self.costMatrix[1][1]
            
            m = Munkres()
            indexes = m.compute(self.costMatrix2)
            #print_matrix(self.costMatrix, msg='Lowest cost through this matrix:')
            total = 0
            for row, column in indexes:
                value = self.costMatrix2[row][column]
                total += value
                #print '(%d, %d) -> %d' % (row, column, value)
                if (column==0):
                    self.all_agents[row].goal= obs.cps[1][0:2]
                elif (column==1):
                    self.all_agents[row].goal= obs.cps[0][0:2]
                elif (column==2):
                    self.all_agents[row].goal= self.AP[0]
                else:
                    self.all_agents[row].goal= self.AP[1]
        #shoot = True
        #check if we dont own any cp (cps: (x,y,flag))
        elif ( obs.cps[1][2] != self.team and obs.cps[0][2] != self.team ):   
            #flags:
            #0 -> red
            #1 -> blue
            #2 -> neutral
            #print obs.cps[1][2]  
            #print self.team      
            #path for bottom cp for agent 0
            #self.path1=find_path(self.all_agents[0].observation.loc, obs.cps[0][0:2], self.mesh, self.grid, self.settings.tilesize)
            #path for top cp for agent 0
            x=0;
            for id in self.all_agents:
                #top cp
                path1=find_path(id.observation.loc, obs.cps[1][0:2], self.mesh, self.grid, self.settings.tilesize)
                #bottom cp
                path2=find_path(id.observation.loc, obs.cps[0][0:2], self.mesh, self.grid, self.settings.tilesize)
                #left ammo
                path3=find_path(id.observation.loc, obs.cps[1][0:2], self.mesh, self.grid, self.settings.tilesize)
                #right ammo
                # path4=find_path(id.observation.loc, self.AP[1], self.mesh, self.grid, self.settings.tilesize)
                print(x,id)
                print(x,self.costMatrix[x])
                self.costMatrix [x][0] = 0.1*self.get_path_length(id.observation.loc,path1)
                self.costMatrix [x][1] = 0.1*self.get_path_length(id.observation.loc,path2)
                self.costMatrix [x][2] = 0.1*self.get_path_length(id.observation.loc,path3)
                # self.costMatrix [x][3] = 0.4*self.get_path_length(id.observation.loc,path4)
                
                x=x+1
            # print self.costMatrix
            ##print self.costMatrix[1][1]
            
            m = Munkres()
            indexes = m.compute(self.costMatrix)
            #print_matrix(self.costMatrix, msg='Lowest cost through this matrix:')
            total = 0
            for row, column in indexes:
                value = self.costMatrix[row][column]
                total += value
                #print '(%d, %d) -> %d' % (row, column, value)
                if (column==0):
                    self.all_agents[row].goal= obs.cps[1][0:2]
                elif (column==1):
                    self.all_agents[row].goal= obs.cps[0][0:2]
                elif (column==2):
                     self.all_agents[row].goal= obs.cps[1][0:2]
#                else:
#                    self.all_agents[row].goal= self.AP[1]
                #print 'goal : ', self.all_agents[row].goal
                #print 'agent : ', row
            #print 'total cost: %d' % total

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
            
        else:# ((obs.loc==self.AP[0] or obs.loc==self.AP[1] and obs.ammo > 0 and obs.foes)): #reached whatever goal it was:
            speed=0
            turn=0
            #turn = angle_fix(math.atan2(dy, dx) - obs.angle)
         #   a=1
        
        return (turn,speed,shoot)
    def action_hung(self):
        turn = 0
        speed = 0
        shoot = False

        
        obs = self.observation  
        #print(self.role)
        
        
        
        #set goals according to roles:
        '''
        if(self.role == 0): #left ammo self.AP[0]
            self.goal = self.AP[0]#(152,151)
            
            #up
            if(point_dist((152,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,111)
            #down
            if(point_dist((152,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,151)
            
        if(self.role == 3): #right ammo self.AP[1]
            self.goal = self.AP[1]#(312,151)
            
            #up
            if(point_dist((312,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,111)
            #down
            if(point_dist((312,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,151)
            
        if(self.role == 1): #bot cp
            self.goal = obs.cps[0][0:2]
        if(self.role == 4):#top cp
            self.goal = obs.cps[1][0:2]
            
        if(self.role == 2): #go to right ammo
            self.goal = self.AP[1]
        if(self.role == 5): #go to left ammo
            self.goal = self.AP[0]
            
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
        else: #( obs.cps[1][2] != self.team and obs.cps[0][2] != self.team):
            #flags:
            #0 -> red
            #1 -> blue
            #2 -> neutral
            #print obs.cps[1][2]  
            #print self.team      
            #path for bottom cp for agent 0
            #self.path1=find_path(self.all_agents[0].observation.loc, obs.cps[0][0:2], self.mesh, self.grid, self.settings.tilesize)
            #path for top cp for agent 0
            x=0;
            for id in self.all_agents:
                #top cp
                path1=find_path(id.observation.loc, obs.cps[1][0:2], self.mesh, self.grid, self.settings.tilesize)
                #bottom cp
                path2=find_path(id.observation.loc, obs.cps[0][0:2], self.mesh, self.grid, self.settings.tilesize)
                #left ammo
                path3=find_path(id.observation.loc, self.AP[0], self.mesh, self.grid, self.settings.tilesize)
                #right ammo
                path4=find_path(id.observation.loc, self.AP[1], self.mesh, self.grid, self.settings.tilesize)

                self.costMatrix [x][0] = 0.1*self.get_path_length(id.observation.loc,path1)
                self.costMatrix [x][1] = 0.1*self.get_path_length(id.observation.loc,path2)
                self.costMatrix [x][2] = 0.4*self.get_path_length(id.observation.loc,path3)
                self.costMatrix [x][3] = 0.4*self.get_path_length(id.observation.loc,path4)

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
                    self.all_agents[row].goal= obs.cps[1][0:2]
                elif (column==1):
                    self.all_agents[row].goal= obs.cps[0][0:2]
                elif (column==2):
                    self.all_agents[row].goal= self.AP[0]
                elif (column==3):
                    self.all_agents[row].goal= self.AP[1]
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
         
            
            
        elif ((obs.loc==self.AP[0] or obs.loc==self.AP[1] and obs.ammo > 0 and obs.foes)): #reached whatever goal it was:
            speed=0
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            a=1
        
        return (turn,speed,shoot)

    def action_t_600(self):
        turn = 0
        speed = 0
        shoot = False


        obs = self.observation
        #print(self.role)



        #set goals according to roles:

        if(self.role == 0): #right ammo self.AP[0]
            self.goal = self.AP[1]#(152,151)
            '''
            #up
            if(point_dist((152,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,111)
            #down
            if(point_dist((152,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,151)
            '''
        if(self.role == 3): #left ammo self.AP[1]
            self.goal = self.AP[0]#(312,151)
            '''
            #up
            if(point_dist((312,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,111)
            #down
            if(point_dist((312,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,151)
            '''
        if(self.role == 1): #bot cp
            self.goal = obs.cps[0][0:2]
        if(self.role == 4):#top cp
            self.goal = obs.cps[1][0:2]

        if(self.role == 2): #go to right ammo
            self.goal = self.AP[1]
        if(self.role == 5): #go to left ammo
            self.goal = self.AP[0]

        #if(self.role == 6): #go to right ammo
            #self.goal = self.AP[1]#(320,250)
        #if(self.role == 7): #go to left ammo
            #self.goal = self.AP[0]#(150,136)
            #####
            #####
        #check if there:




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

        # Shoot enemies
        shoot = False
        if (obs.ammo > 0 and obs.foes and point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True



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
            '''if(self.role < 5 and self.role >= 0):
                self.role += 1
            else:
                self.role = 0
            '''
            if (self.role == 0): ##2,4
                self.role = 4

            elif (self.role == 1): ##2,4
                self.role = 3

            elif (self.role == 2): ##2,4
                self.role = 5

            elif (self.role == 3):
                self.role = 0

            elif (self.role == 4):
                self.role = 2

            elif (self.role == 5):
                self.role = 1

            '''
            if(self.role == 1 or self.role == 4):#reached the cp
                self.role += 1
            elif(self.role == 5):#clap with other agent
                for i in range(len(self.all_agents)):
                    if(self.all_agents[i].role == 0): #change others agants role !
                        self.all_agents[i].role = 1
                self.role = 0

            elif(self.role == 2): #clap with other agent
                for i in range(len(self.all_agents)):
                    if(self.all_agents[i].role == 3):
                        self.all_agents[i].role = 4
                        break
                self.role = 3
            '''
        '''
        if(self.id == 1 and not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        '''
        '''
        if(self.id == 2 and not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        '''

        #if(self.id = 0 and not obs.loc == self.goal):
        #    pass


        #if(self.id == 0):
        #    print(turn,speed,self.id)
        return (turn,speed,shoot)

    
    
    
    def action_det_ag2(self):
        turn = 0
        speed = 0
        shoot = False

        
        obs = self.observation  
        #print(self.role)
        
        
        
        #set goals according to roles:
        
        if(self.role == 0): #left ammo self.AP[0]
            self.goal = self.AP[0]#(152,151)
            '''
            #up
            if(point_dist((152,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,111)
            #down
            if(point_dist((152,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (152,151)
            '''
        if(self.role == 3): #right ammo self.AP[1]
            self.goal = self.AP[1]#(312,151)
            '''
            #up
            if(point_dist((312,151), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,111)
            #down
            if(point_dist((312,111), obs.loc) < self.settings.tilesize-3):
                self.goal = (312,151)
            '''
        if(self.role == 1): #bot cp
            self.goal = obs.cps[0][0:2]
        if(self.role == 4):#top cp
            self.goal = obs.cps[1][0:2]
            
        if(self.role == 2): #go to right ammo
            self.goal = self.AP[1]
        if(self.role == 5): #go to left ammo
            self.goal = self.AP[0]
            
        #if(self.role == 6): #go to right ammo
            #self.goal = self.AP[1]
        #if(self.role == 7): #go to left ammo
            #self.goal = self.AP[0]
            #####
            #####
        #check if there:

        
        

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
        
        # Shoot enemies
        shoot = False
        if (obs.ammo > 0 and obs.foes and point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True
            


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
            '''if(self.role < 5 and self.role >= 0):
                self.role += 1
            else:
                self.role = 0
            '''
            if (self.role == 0):
                self.role = 3
            
            elif (self.role == 1):
                self.role = 4
            
            elif (self.role == 2):
                self.role = 4
                         
            elif (self.role == 3):
                self.role = 0
            
            elif (self.role == 4):
                self.role = 1
            
            elif (self.role == 5):
                self.role = 1
            
            '''
            if(self.role == 1 or self.role == 4):#reached the cp
                self.role += 1
            elif(self.role == 5):#clap with other agent
                for i in range(len(self.all_agents)):
                    if(self.all_agents[i].role == 0): #change others agants role !
                        self.all_agents[i].role = 1
                self.role = 0
                
            elif(self.role == 2): #clap with other agent
                for i in range(len(self.all_agents)):
                    if(self.all_agents[i].role == 3):
                        self.all_agents[i].role = 4
                        break
                self.role = 3
            '''
        '''
        if(self.id == 1 and not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        '''
        '''
        if(self.id == 2 and not point_dist(self.goal, obs.loc) < self.settings.tilesize):
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        '''
        
        #if(self.id = 0 and not obs.loc == self.goal):
        #    pass
    
            
        #if(self.id == 0):
        #    print(turn,speed,self.id)
        return (turn,speed,shoot)

    def action_agent(self):
        obs = self.observation
        # Check if agent reached goal.
        if self.goal is not None and point_dist(self.goal, obs.loc) < self.settings.tilesize:
            self.goal = None
            
        # Walk to ammo
        ammopacks = filter(lambda x: x[2] == "Ammo", obs.objects)
        if ammopacks:
            self.goal = ammopacks[0][0:2]
            
        # Drive to where the user clicked
        # Clicked is a list of tuples of (x, y, shift_down, is_selected)
        if self.selected and self.observation.clicked:
            self.goal = self.observation.clicked[0][0:2]
        
        # Walk to random CP
        if self.goal is None:
            self.goal = obs.cps[random.randint(0,len(obs.cps)-1)][0:2]
        
        # Shoot enemies
        shoot = False
        if (obs.ammo > 0 and 
            obs.foes and 
            point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and
            not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True

        # Compute path, angle and drive
        path = find_path(obs.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
        if path:
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        else:
            turn = 0
            speed = 0
        #turn = 0
        #speed = 0
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
        
        self.result = 0
        
        if (self.id == 0):
            if (self.observation.score[self.team] >= 50):
                self.result = 1
                self.gamwinpol = [self.gamwinpol[0]+1,self.gamwinpol[1]+1,self.policy]
                print("wongame")
            else:
                self.gamwinpol = [self.gamwinpol[0]+1,self.gamwinpol[1],self.policy]
                self.result = 0
            
            
        #try:    
            #newdata = self.policy, self.result
            #self.memory.append(newdata)
            #print "final:", self.memory
            pickle.dump(self.gamwinpol, open("tmemory.p","wb"))
            print "Blob Written!"
        #except:
        #    print "Blob write error: Make sure to have Write Access!"
        pass
