import pickle
from domination import core
rp = pickle.load(open('replay20130220-1441_t3v6_vs_t5v6.pickle','rb'))
print rp
rp.play()