import cPickle as pickle
import math


'''
converts the joint action to an index for the q_vals
'''
def serialize(action0,action1,action2):
    return(25*action0+5*action1+action2)
'''
converts action index to actions
'''
def de_serialize(no):
    #print("de_serializing:",no)
    action0 = int(math.floor(no/25))
    action1 = int(math.floor(no/5)%5)
    action2 = int(no%5)
    return([action0,action1,action2])


print("started")
'''
sa0 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa1 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa2 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
'''
'''
sa0 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa1 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa2 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
'''
'''
standard wolf
qtable0 = [[[[[[[[[0.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
qtable1 = [[[[[[[[[0.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
qtable2 = [[[[[[[[[0.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 

avrg_policy0 = [[[[[[[[[0.2 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
avrg_policy1 = [[[[[[[[[0.2 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
avrg_policy2 = [[[[[[[[[0.2 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 

policy0 = [[[[[[[[[0.2 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
policy1 = [[[[[[[[[0.2 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
policy2 = [[[[[[[[[0.2 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 

state_counter0 = [[[[[[[[0 for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
state_counter1 = [[[[[[[[0  for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
state_counter2 = [[[[[[[[0  for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 


info0 = [qtable0,avrg_policy0,policy0,state_counter0]
#info1 = [qtable1,avrg_policy1,policy1,state_counter1]
#info2 = [qtable2,avrg_policy2,policy2,state_counter2]
#total =[info0,info1,info2] # pickle.load(open("stateActionValues-reduced.p3","rb"))

'''


#joint action wolf

qtable0 = [[[[[[[[[0.0 for actions in range(0,125)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
avrg_policy0 = [[[[[[[[[1.0/125.0 for actions in range(0,125)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
policy0 = [[[[[[[[[1.0/125.0 for actions in range(0,125)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
state_counter0 = [[[[[[[[0  for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 

counter = 0
total = 0
for s0 in range(0,5):
    for a0 in range(0,2):
        print(s0,a0)
        for s1 in range(0,5):
            for a1 in range(0,2):
                for s2 in range(0,5):
                    for a2 in range(0,2):
                        for cp0 in range(0,3):
                            for cp1 in range(0,3):
                                counter2 = 0
                                total2 = 0
                                for a in range(0,125):
                    
                                    res = de_serialize(a)
                                    if(res[0]==4 or res[1]==4 or res[2] == 4 ):
                                        counter2 += 1
                                        total2 +=1
                                        counter += 1
                                        total +=1
                                        avrg_policy0[s0][a0][s1][a1][s2][a2][cp0][cp1][a] = 0
                                        policy0[s0][a0][s1][a1][s2][a2][cp0][cp1][a] = 0
                                    else:
                                        total2 +=1
                                        total += 1
                                        avrg_policy0[s0][a0][s1][a1][s2][a2][cp0][cp1][a] += (1.0/125.0)* 61.0/64.0
                                        policy0[s0][a0][s1][a1][s2][a2][cp0][cp1][a] += (1.0/125.0)*61.0/64.0  
for s0 in range(0,5):
    for a0 in range(0,2):
        print(s0,a0)
        for s1 in range(0,5):
            for a1 in range(0,2):
                for s2 in range(0,5):
                    for a2 in range(0,2):
                        for cp0 in range(0,3):
                            for cp1 in range(0,3):
                                summ = 0
                                sumn = 0
                                for a in range(0,125):
                                    summ += policy0[s0][a0][s1][a1][s2][a2][cp0][cp1][a]
                                    sumn += avrg_policy0[s0][a0][s1][a1][s2][a2][cp0][cp1][a]
                                if(not((summ == 1.0) or (sumn == 1.0))):
                                    print("not 1!",summ,sumn) 
       
                                        

print("removed:",counter,"from:",total)
info0 = [qtable0,avrg_policy0,policy0,state_counter0,0]
#info1 = [qtable1,avrg_policy1,policy1,state_counter1]
#info2 = [qtable2,avrg_policy2,policy2,state_counter2]
#total =[info0,info1,info2] # pickle.load(open("stateActionValues-reduced.p3","rb"))
pickle.dump(info0, open("wolf-tables_joint.p","wb"))
print("finished")