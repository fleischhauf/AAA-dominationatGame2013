import pickle

print("started")
'''
sa0 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa1 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa2 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
'''
sa0 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa1 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 
sa2 = [[[[[[[[[10.0 for move in range(0,5)] for cp2 in range(0,3)] for cp1 in range(0,3)]for hasAmmo3 in range(0,2)] for states3 in range(0,5)]for hasAmmo2 in range(0,2)] for states2 in range(0,5)]for hasAmmo1 in range(0,2)]  for states1 in range(0,5)] 


#sa = pickle.load(open())
actionValues_total =[sa0,sa1,sa2,0] # pickle.load(open("stateActionValues-reduced.p3","rb"))
pickle.dump(actionValues_total, open("stateActionValues-reduced.p","wb"))
print("finished")
