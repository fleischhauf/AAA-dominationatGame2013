import math
from domination import core
from domination import run

FIELD = """
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ w _ C _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ w _ _ _ w w w w w w w w w w w _ _ _ _ _ _ w
w _ _ w _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ w
w R _ w _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ B w
w R _ w _ _ _ w _ A _ _ w w w w w _ _ A _ w _ _ _ w _ B w
w R _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ w _ B w
w _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ w _ _ w
w _ _ _ _ _ _ w w w w w w w w w w w _ _ _ w _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ C _ w _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
"""
#Commit test by john.
class Tournament1(run.Scenario):
    GENERATOR = None
    FIELD     = core.Field.from_string(FIELD)
    #SETTINGS  = core.Settings(ammo_amount=2, spawn_time=10, ammo_rate=14, max_see=70, max_turn=math.pi/4, max_score=10000)
    SETTINGS = core.Settings(think_time=0.0625, ammo_rate=9, ammo_amount=1, max_score=100, max_see=70)


#Tournament1.one_on_one(red="domination/agent.py", blue="domination/agent.py", output_folder='_tmp')
Tournament1.test(red="domination/deterministic_agent2.py", blue="domination/agent.py")
