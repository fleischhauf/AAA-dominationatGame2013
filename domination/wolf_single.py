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
        if blob is not None and self.id == 0:
            # Remember the blob path so we can write back to it
            self.blobpath = blob.name
            self.blobcontent = pickle.loads(blob.read())
            print "Agent %s received binary blob of %s" % (
               self.callsign, type(self.blobcontent))
            # Reset the file so other agents can read it too.
            blob.seek(0) 
            
        # Recommended way to share variables between agents.
        if id == 0:
            self.all_agents = self.__class__.all_agents = []
        self.all_agents.append(self)

        self.CP_UP = 0
        self.CP_DOWN = 1
        self.AMMO_1 = 2
        self.AMMO_2 = 3
        self.SPAWN_FR = 4
        #self.SPAWN_EN = 5
        
        self.sa_vals = 0
        self.avrg_policy = 0
        self.policy = 0
        self.state_counter = 0
        
        if(self.id == 0):
            self.sa_vals = pickle.load(blob)
            self.stateActionValues = self.sa_vals[0][0]
            self.avrg_policy = self.sa_vals[0][1]
            self.policy = self.sa_vals[0][2]
            self.state_counter = self.sa_vals[0][3]
        if(self.id == 1):
            self.stateActionValues = self.all_agents[0].sa_vals[1][0]
            self.avrg_policy = self.all_agents[0].sa_vals[1][1]
            self.policy = self.all_agents[0].sa_vals[1][2]
            self.state_counter = self.all_agents[0].sa_vals[1][3]
        if(self.id == 2):
            self.stateActionValues = self.all_agents[0].sa_vals[2][0]
            self.avrg_policy = self.all_agents[0].sa_vals[2][1]
            self.policy = self.all_agents[0].sa_vals[2][2]
            self.state_counter = self.all_agents[0].sa_vals[2][3]

        self.ACTIONS = [(232,56),(264,216),(184,168),(312, 104),(40,180)]#,(440,90)]

        self.action_taken = self.SPAWN_FR
        self.old_state = [self.SPAWN_FR,0,self.SPAWN_FR,0,self.SPAWN_FR,0,0,0] #assuming cp1 and 2 are not owned: 2, taken by blue : 1
        self.current_state  = self.old_state
        self.my_state = [self.SPAWN_FR,0] #state, ammo
        self.first_run = True
        self.score_old = 0
        self.score_cur = 0
        
        #assume we start at our spawn point
        self.loc = self.ACTIONS[self.SPAWN_FR] 
        self.last_loc = self.loc
        
        #q learning variables:
        self.LR = 0.8
        self.DISCOUNT = 0.9
        
        
        #wolf variables amog vals:
        self.DELTAW = 0.01
        self.DELTAI = 0.05
        
        
        self.reward = 0.0
        #for i in range(0,1000):
        #    print(self.wolf_select_action())
        
        
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
            
        transition_complete = self.check_transition()
        
        me_has_ammo = 0
        if(self.observation.ammo > 0):
            me_has_ammo = 1
        
        if(transition_complete):
            self.my_state = [self.action_taken,me_has_ammo]
        else:
            if(self.id == 0):
                self.my_state = [self.old_state[0],me_has_ammo]
            if(self.id == 1):
                self.my_state = [self.old_state[2],me_has_ammo]
            if(self.id == 2):
                self.my_state = [self.old_state[4],me_has_ammo]
    
    
    
    '''
    finds action with maximum value out of q-value table
    '''
    def get_max_action(self,current_state):
        max_val = -10000
        max_action = -1
        #pos_x = self.current_state[0]
        #pos_y = self.current_state[1]

        #print("ACTIONMATRIX")
        
        #print("get max action",current_state," length",len(self.stateActionValues[current_state[0]][current_state[1]]))
        for action in range(0,5):
            if(self.stateActionValues[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][current_state[5]][current_state[6]][current_state[7]][action] > max_val):
                max_val = self.stateActionValues[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][current_state[5]][current_state[6]][current_state[7]][action]
                max_action = action
        #print("max at ",x,y,max_val)
        return([max_action,max_val])
    
    '''
    does wolf
    '''
    def wolf(self):
        ######update estimate of avg. policy:######
        #C(s) ++
        self.state_counter[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]] += 1
        c = self.state_counter[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]]
        # update avg.policy
        for a in range(0,5):
            policy = self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]
            avrg_policy = self.avrg_policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]
            self.avrg_policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a] += 1 / float(c) * (policy - avrg_policy )
        
        ######update pi(s,*) with stepsize delta towards best Q-value
        # determine which delta to use
        delta = 0
        sum_avrg = 0
        sum_policy = 0
        for a in range(0,5):
            prob_pol = self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]
            prob_avrg = self.avrg_policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]
            val = self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]
            
            sum_policy += prob_pol * val
            sum_avrg += prob_avrg * val
        #determine delta
        if(sum_policy > sum_avrg):
            delta = self.DELTAW
        else:
            delta =  self.DELTAI
        # update policies with stepsize delta twoards the best Q-value:
        
        res = self.get_max_action(self.current_state) 
        max_action = res[0]
        for a in range(0,5):
            if(a == max_action):
                self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a] += delta 
            else:
                self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a] -= delta / 4.0
        
        #check for wrong values!!
        # prob >= 0 and sum (p) == 1
        sum_probs = 0
        for a in range(0,5):
            prob = self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]
            if(prob < 0 ):
                self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]= 0
                prob = 0
            if(prob > 1):
                self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][a]= 1
                prob = 1
                
            sum_probs +=  prob
        if(sum_probs > 1 or sum_probs < 0):
            r = random.randint(0,4)
            self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][r] -= (sum_probs -1)
            print("sum of probabilities is wrong:",sum_probs)
        
        
        print("for max values for agent ",self.id," :",self.current_state)
        
        for l in range(0,len(self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]])):
        
            '''
            cps_UP: 232,56
            cps_DOWN: 264,216
            ammo_1: 184,168
            ammo_2: 312, 104 (enemy)
            spawn_FR: 40,180
            spawn_EN: 440,90
            '''
            
            if(l == 0):
                print("CPS_UP:",self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 1):
                print("CPS_DO:",self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 2):
                print("AMMO_1:",self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 3):
                print("AMMO_2:",self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 4):
                print("SPAWNR:",self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 5):
                print("SPAWNO:",self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
        
        #self.CP_UP = 0
        #self.CP_DOWN = 1
        #self.AMMO_1 = 2
        #self.AMMO_2 = 3
        #self.SPAWN_FR = 4
        #self.SPAWN_EN = 5
        
        
    
    '''
    selects action using deterministic policy
    '''
    def wolf_select_action(self):
        r = random.randrange(0,1000)/1000.0
        
        b0 = self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][0]
        b1 = b0 + self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][1]
        b2 = b1 + self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][2]
        b3 = b2 + self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][3]
        b4 = b3 + self.policy[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][4]
        print("random number:",r)
        if(0 <= r and r < b0):
            return(0)
        elif(b0  <= r and r < b1):
            return(1)
        elif(b1 < r and r <= b2):
            return(2)
        elif(b2 < r and r <= b3):
            return(3)
        elif(b3 < r and r <= 1):
            return(4)

   
    
    '''
    update Q-table updates q-table, only if transition successful and complete
    '''
    def update_q_table(self):
        #learning:
        #future_reward = self.stateActionValues[self.current_state[0] ] [ ][x][y]
        #old_value = self.stateActionValues[self.old_state[0] ] [ self.old_state[1]][self.action_taken[0]][self.action_taken[1]]
        #self.stateActionValues[self.old_state[0] ] [ self.old_state[1]][self.action_taken[0]][self.action_taken[1]] += self.LR * (reward + self.DISCOUNT * future_reward - old_value  )
        res = self.get_max_action(self.current_state)
        next_action = res[0]
        
        #print("qtable old_state",self.old_state)
        future_reward = self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][next_action] #check if last action 
        old_value = self.stateActionValues[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_state[5]][self.old_state[6]][self.old_state[7]][self.action_taken]
        
        self.stateActionValues[self.old_state[0]][self.old_state[1]][self.old_state[2]][self.old_state[3]][self.old_state[4]][self.old_state[5]][self.old_state[6]][self.old_state[7]][self.action_taken ] = old_value +  self.LR * (self.reward + self.DISCOUNT * future_reward - old_value  )
        
        #DEBUG :
        '''
        print("for max values for agent ",self.id," :",self.current_state)
        
        for l in range(0,len(self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]])):
        '''
        '''
            cps_UP: 232,56
            cps_DOWN: 264,216
            ammo_1: 184,168
            ammo_2: 312, 104 (enemy)
            spawn_FR: 40,180
            spawn_EN: 440,90
        '''
        '''    
            if(l == 0):
                print("CPS_UP:",self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 1):
                print("CPS_DO:",self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 2):
                print("AMMO_1:",self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 3):
                print("AMMO_2:",self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 4):
                print("SPAWNR:",self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
            if(l == 5):
                print("SPAWNO:",self.stateActionValues[self.current_state[0]][self.current_state[1]][self.current_state[2]][self.current_state[3]][self.current_state[4]][self.current_state[5]][self.current_state[6]][self.current_state[7]][l])
        
        #self.CP_UP = 0
        #self.CP_DOWN = 1
        #self.AMMO_1 = 2
        #self.AMMO_2 = 3
        #self.SPAWN_FR = 4
        #self.SPAWN_EN = 5
        '''
    '''
    check if transition is complete
    '''
    def check_transition(self):
        #print(self.ACTIONS[self.action_taken])
        if( point_dist(self.loc, self.ACTIONS[self.action_taken]) < self.settings.tilesize ):
            return(True)
        else:
            return(False)
    

    def action(self):
        """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """
        
        #check if transition is complete:
        self.loc = self.observation.loc
        
        transition_complete = self.check_transition()
        
        #calculate dynamic reward according to game score:
        if(self.first_run):
            self.score_cur = self.observation.score[0]
            self.first_run = False
        else:
            self.score_cur = self.observation.score[0]
            self.reward += self.score_cur - self.score_old
            #print(self.reward," cur:",self.score_cur," old:", self.score_old)
        
        
        #if transition complete, learn something!        
        if(transition_complete ):
            #print("transition complete")
            self.goal = self.loc
            #check control points:
            cps = self.observation.cps
            #not taken by blue
            cp1 = cps[0][2]

            cp2 = cps[1][2]

            if(self.id == 0):
                he = self.all_agents[1]
                she = self.all_agents[2]
                self.current_state = [self.my_state[0],self.my_state[1],he.my_state[0],he.my_state[1],she.my_state[0],she.my_state[1],cp1,cp2]
            if(self.id == 1):
                he = self.all_agents[0]
                she = self.all_agents[2]
                self.current_state = [he.my_state[0],he.my_state[1],self.my_state[0],self.my_state[1],she.my_state[0],she.my_state[1],cp1,cp2]
            if(self.id == 2):
                he = self.all_agents[0]
                she = self.all_agents[1]
                self.current_state = [he.my_state[0],he.my_state[1],she.my_state[0],she.my_state[1],self.my_state[0],self.my_state[1],cp1,cp2]

            #do learning!
            '''
            self.update_q_table()
            
            res = self.get_max_action(self.current_state)
            
            self.action_taken = res[0]
            '''
            
            #update using wolf
            
            #first update q-table
            self.update_q_table()
            self.wolf()
            
            #choose action
            self.action_taken = self.wolf_select_action()

            self.goal = self.ACTIONS[self.action_taken]
            
            #reset reward
            self.reward = 0.0
        else:
            #print("transition not complete")
            self.goal = self.ACTIONS[self.action_taken]


        #convert goal to range and bearing
        turn = 0
        speed = 0
        shoot = False
        #take action
        #print("new goal:",self.goal)
        obs = self.observation
        if (obs.ammo > 0 and 
            obs.foes and 
            point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and
            not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True
 
        if(not self.goal == None):
            path = find_path(self.observation.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
            if path:
                dx = path[0][0] - self.observation.loc[0]
                dy = path[0][1] - self.observation.loc[1]
                turn = angle_fix(math.atan2(dy, dx) - self.observation.angle)
                if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                    shoot = False
                speed = (dx**2 + dy**2)**0.5
                if turn > self.settings.max_turn or turn < -self.settings.max_turn and point_dist(self.loc,self.goal)< self.settings.max_speed:
                    speed = 0
            else:
                turn = 0
                speed = 0
                
        self.last_loc = self.loc
        self.old_state = self.current_state
        
        self.score_old = self.score_cur


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

        p1 = path2[0]
        p2 = path2[1]
        p3 = path2[2]
        
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
        #first agents saves everything!
        if(self.id == 0):
            print("FINALIZING")
            
            won = 1
            if(self.score_cur <= 50):
                won = 0
                
                
            qtable0 =  self.all_agents[0].stateActionValues
            qtable1 =  self.all_agents[1].stateActionValues
            qtable2 =  self.all_agents[2].stateActionValues
            avrg_policy0 = self.all_agents[0].avrg_policy
            avrg_policy1 = self.all_agents[1].avrg_policy
            avrg_policy2 = self.all_agents[2].avrg_policy
            policy0 = self.all_agents[0].policy
            policy1 = self.all_agents[1].policy
            policy2 = self.all_agents[2].policy
            state_counter0 = self.all_agents[0].state_counter
            state_counter1 = self.all_agents[1].state_counter
            state_counter2 = self.all_agents[2].state_counter
            
            info0 = [qtable0,avrg_policy0,policy0,state_counter0]
            info1 = [qtable1,avrg_policy1,policy1,state_counter1]
            info2 = [qtable2,avrg_policy2,policy2,state_counter2]
            total =[info0,info1,info2]

            pickle.dump(total, open(self.blobpath,"wb"))
            #r = random.randint(0,5)
            #pickle.dump(total, open("wolf-tables.p"+str(r),"wb"))
            print("written pickle")
        pass
        

