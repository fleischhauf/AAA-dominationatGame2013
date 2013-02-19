import random

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
        
        
        
        
        #state space: [agent_0][agent_1][agent_2][ammo0][ammo1][cp0][cp1][hasAmmo][action]    #[seesEnemy?]
        '''
        so this should be correct, since it does not matter which agent is in which tile, we specify active agent as agent_0
        and update the state_action_vals policy and avg_policy accordingly for all agents.
        '''
        if(self.id == 0):
            self.state_action_vals = [[[[[[[[[.0]*5]*2]*2]*2]*2]*2]*5]*5]*5
            self.policy = [[[[[[[[[.2]*5]*2]*2]*2]*2]*2]*5]*5]*5
            self.avg_policy = [[[[[[[[[.2]*5]*2]*2]*2]*2]*2]*5]*5]*5
            self.count = [[[[[[[[0]*2]*2]*2]*2]*2]*5]*5]*5
        #defines world state the agent is currently in
        self.world_state_new = []
        self.world_state_old = []
        self.action_old = []

        self.region = -1



        
        #defines the reward
        '''
        so either we:
        1. take the global stats, 
        or 
        2. we assign immidiate rewards for different state transitions
        which would bring the problem, that the priorities are predefined. 
        or
        3. include both, such that getting ammo and conquering cp have an advantage i.e. push the agent to the right actions
        -->how model kill an opponent?
        '''
        self.reward = 0.0
        
        
        
        #points of interest and actions
        #constants
        self.CAMP = (36,82)
        self.CP_UP = (220, 56)
        self.CP_BOT = (248, 216)
        self.AMMO_LEFT = (152,136)
        self.AMMO_RIGHT = (312,136)
        
        self.POI = [self.CAMP,self.CP_UP,self.CP_BOT,self.AMMO_LEFT,self.AMMO_RIGHT]

        
        self.CAMP_NO = 0
        self.CP_UP_NO = 1
        self.CP_BOT_NO = 2
        self.AMMO_LEFT_NO = 3
        self.AMMO_RIGHT_NO = 4
        
        self.ACTIONS = [self.CAMP_NO,self.CP_UP_NO,self.CP_BOT_NO,self.AMMO_LEFT_NO,self.AMMO_RIGHT_NO]  
        
        #wolf parameters:
        self.ALPHA = 0.5
        self.DELTA_L = 0.01
        self.DELTA_W = 0.001
        self.GAMMA = 0.9
        
        #if first run
        self.run_no = 0
        
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
            print("id:",self.id)
            print observation
            
    '''
    moves to selected goal
    '''
    def get_turn_speed_shoot(self):
        #goto goal!
        shoot = False
        obs = self.observation
        path = find_path(obs.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
        #print(self.id,"i keep movin movin movin")
        dx = path[0][0] - obs.loc[0]
        dy = path[0][1] - obs.loc[1]
        turn = angle_fix(math.atan2(dy, dx) - obs.angle)
        if turn > self.settings.max_turn or turn < -self.settings.max_turn:
            shoot = False
        if(not shoot and (dx**2 + dy**2) > self.settings.max_speed):
            speed = (dx**2 + dy**2)**0.5
        else:
            speed = 0
        return([turn,speed])           
    
    
    '''
    finds region of interest as in state space
    '''
    def find_region(self,obs):
        #arg_min pointsofinterest (dist to point from loc)
        min_length = 10000
        closest_poi = (0,0)
        length = 0
        for p in self.POI:
            path = find_path(obs.loc, p, self.mesh, self.grid, self.settings.tilesize)
            length  = self.get_path_length(obs,path)
            if(length < min_length):
                min_length = length
                closest_poi = p
                
        state_number = -1
        if(closest_poi == self.CAMP):
            state_number = self.CAMP_NO
        elif(closest_poi == self.CP_UP):
            state_number = self.CP_UP_NO
        elif(closest_poi == self.CP_BOT):
            state_number = self.CP_BOT_NO
        elif(closest_poi == self.AMMO_LEFT):
            state_number = self.AMMO_LEFT_NO
        elif(closest_poi == self.AMMO_RIGHT):
            state_number = self.AMMO_RIGHT_NO

        return([state_number,closest_poi,min_length])
        #ammo_left, ammo_right, cp_up, cp_down,camp point
        #interest_points = [(152,136),(312,136),(220, 56),(248, 216),(,)]        
    
    
    '''
    finds the length of the path
    '''
    def get_path_length(self,obs,path):
        current_pos = obs.loc
        length = 0
        for point in path:
            dx = point[0] - current_pos[0]
            dy = point[1] - current_pos[1]
            length += math.sqrt(dx*dx + dy*dy)
            current_pos = point
            
        return(length)
    
    
    '''
    find max action according to given action values from state_action_value space
    '''
    def wolf_find_max_a(self,action_values):
        max = -1000
        max_a = -1
        for a in self.ACTIONS:
            if(action_values[a] > max):
                max = action_values[a]
                max_a = a
                
        return(max_a)

    '''
    find max action value according to given action values from state_action_value space
    '''
    def wolf_find_max_a_val(self,action_values):
        max = -1000
        for a in self.ACTIONS:
            if(action_values[a] > max):
                max = action_values[a]
        return(max)
    
    
    '''
    selects action according to probabilistic policy
    '''
    def wolf_select_action(self):
        rand_uniform = random.random()
        #print(rand_uniform)
        #policy probabilities
        #print(self.current_state)
        pp =  self.all_agents[0].policy[self.world_state_new[0]][self.world_state_new[1]][self.world_state_new[2]][self.world_state_new[3]][self.world_state_new[4]][self.world_state_new[5]][self.world_state_new[6]][self.world_state_new[7]]
        #print(pp)
        action_no = -1
        #print(rand_uniform,pp[0],pp[1],pp[2],pp[3],pp[4])
        if(rand_uniform < pp[0]):
            self.goal = self.CAMP
            action_no = self.CAMP_NO
        elif(rand_uniform < pp[0]+pp[1]):
            self.goal = self.CP_UP
            action_no = self.CP_UP_NO
        elif(rand_uniform < pp[0]+pp[1]+pp[2]):
            self.goal = self.CP_BOT
            action_no = self.CP_BOT_NO
        elif(rand_uniform < pp[0]+pp[1]+pp[2]+pp[3]):
            self.goal  =self.AMMO_LEFT
            action_no = self.AMMO_LEFT_NO
        else:
            self.goal = self.AMMO_RIGHT
            action_no = self.AMMO_RIGHT_NO
        return(action_no)
    
    '''
    win or learn fast policy hill climbing.
    '''
    def wolf(self):
        #select action a for state s using policy obtain reward and new state -->done in action and observation
        #happens in self.action()

        cs = self.world_state_new
        os = self.world_state_old
        ###update Q(s,a)= (1-alpha)* Qt(s,a) + alpha(r+ gamma * max a' Qt(s',a'))
        state_action_val  =self.all_agents[0].state_action_vals[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][self.action_old]
        #so this should be: take a from s, observe reward, look for future discounted reward.
        self.all_agents[0].state_action_vals[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][self.action_old] = (1 - self.ALPHA) * state_action_val + self.ALPHA * (self.reward + self.GAMMA * self.wolf_find_max_a_val(self.all_agents[0].state_action_vals[cs[0]][cs[1]][cs[2]][cs[3]][cs[4]][cs[5]][cs[6]][cs[7]]))
        
        
        ### update estimate of avg. policy
        self.all_agents[0].count[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]] += 1
        c = self.all_agents[0].count[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]]
        for b in self.ACTIONS:
            p = self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][b]
            p_avg = self.all_agents[0].avg_policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][b]
            self.all_agents[0].avg_policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][b] += 1/c * (p - p_avg)
    
    
        #Now update policy(s,*) with stepsize delta towards the best Q-value
        #where delta = delta_w if (Pi(s,*) * Q(s,*) > (p_avg(s, *) * Q(s,*)
        sum_avg = 0.0
        sum_p = 0.0
        for a in self.ACTIONS:
            sum_p += self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a]
            sum_avg += self.all_agents[0].avg_policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a]
        delta = 0
        if(sum_p > sum_avg):
            delta = self.DELTA_W
        else:
            delta = self.DELTA_L
        action_vals = self.all_agents[0].state_action_vals[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]]
        max_a = self.wolf_find_max_a(action_vals)
        
        for a in self.ACTIONS:
            # if max action add delta
            if(a == max_a):
                self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a] += delta 
            #otherwise substract fraction of delta
            else:
                self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a] -= delta / (len(self.ACTIONS)-1)
        sum = 0.0
        for a in self.ACTIONS:
            val = self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a]
            sum += val
            if(val > 1):
                #print("fuck you val > 1", val)
                self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a] = 1
            if(val < 0):
                #print("fuck you val < 1",val)
                self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][a] = 0
        if(sum > 1):
            i = random.randrange(0,5)
            self.all_agents[0].policy[os[0]][os[1]][os[2]][os[3]][os[4]][os[5]][os[6]][os[7]][i] += 1.0 -sum
            #print("bigger 1",sum)
            
    
    def action(self):
        """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """

        #init:
        obs = self.observation
        turn = 0
        speed = 0
        shoot = False
        
        
        #new state
        #[agent_0][agent_1][agent_2][ammo0][ammo1][cp0][cp1][hasAmmo][action]
        
        #self.world_state_new = 
        
        
        #perform learning:
        res  = self.find_region(obs)
        self.region = res[0]
        agent_0 = self.all_agents[0].region
        agent_1 = self.all_agents[1].region
        agent_2 = self.all_agents[2].region
        
        #find ammopacks
        ammo0 = 0
        ammo1 = 0
        ammopacks = filter(lambda x: x[2] == "Ammo", obs.objects)
        if ammopacks:
            for pos in ammopacks:
                if(pos[0:2] == self.AMMO_LEFT):
                    ammo0 = 1
                elif(pos[0:2] == self.AMMO_RIGHT):
                    ammo1 = 1
        hasAmmo = 0
        if(obs.ammo > 0):
            hasAmmo = 1
        
        cp0 = 0
        cp1 = 0
        if(obs.cps[0][2] == 2):
            cp0 = 1
        if(obs.cps[1][2] == 2):
            cp1 = 1
        self.world_state_new = [agent_0,agent_1,agent_2,ammo0,ammo1,cp0,cp1,hasAmmo]

        '''
        TODO: EXTEND REWARD SYSTEM:
        '''
        '''
        self.reward = 0
        if(self.world_state_new[5] == 1):
            self.reward +=1
        else:
            self.reward -=1
        if(self.world_state_new[6] == 1):
            self.reward +=1
        else:
            self.reward -=1
        '''
        self.reward = 0.0
        
        if(not(self.world_state_new == [] or self.world_state_old ==[])):

            
            if(self.world_state_old[5] == 0 and self.world_state_new[5] == 1):
                self.reward +=100
            if(self.world_state_old[6] == 0 and self.world_state_new[6] == 1):
                self.reward += 100
        
        #wolf
        if(not(self.world_state_new == [] or self.world_state_old == [])):
            self.wolf()

        #choose action
        a = self.wolf_select_action()
        #backup state
        self.world_state_old = self.world_state_new

        #backup action
        self.action_old = a
        #select action for current state
        #self.goal = (250,40)
        #turn,speed = self.get_turn_speed_shoot()

        
        #compute next goal
        # Compute path, angle and drive
        
        #print("agent: ",self.id," goal : ",a)
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
        
