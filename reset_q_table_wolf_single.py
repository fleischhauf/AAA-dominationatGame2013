import pickle

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

qtable0 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
qtable1 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
qtable2 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 

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
info1 = [qtable1,avrg_policy1,policy1,state_counter1]
info2 = [qtable2,avrg_policy2,policy2,state_counter2]
total =[info0,info1,info2] # pickle.load(open("stateActionValues-reduced.p3","rb"))
pickle.dump(total, open("wolf-tables_single.p","wb"))
print("finished")