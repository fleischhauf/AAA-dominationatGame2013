from domination import core
import math

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

'''
if(self.id == 0):
    self.goal = (152,136)
'''
'''
if(self.id == 0):
    left ammo = (152,136)
if(self.id == 1):
    right ammo  = (312,136)
    ctr bot #(248, 216)
    ctr top #(220, 56)
'''
# Make it a short game
#settings = core.Settings(max_steps=1000)
#These are the oficial settings
settings = core.Settings(think_time=0.0625, ammo_rate=9, ammo_amount=1, max_score=100, max_see=70)
#settings = core.Settings(max_steps=10000,ammo_amount=2,spawn_time=10,ammo_rate=14,max_see=70,max_turn=math.pi/4,max_score=100000)
FI = core.Field.from_string(FIELD)
# Initialize a game
#game = core.Game('domination/agent.py', 'domination/functiontest.py',
score = 0
ammo = 0
enemyammo = 0
kills = 0
deaths = 0
thinktime = 0
steps = 0

for i in range(1, 101):
    game = core.Game('domination/T-600.py', 'domination/agent.py',
                     record=True, rendered=False,verbose=False, settings=settings, field=FI)
    game.run()
    #print game.stats
    print "Game:", i, "| Score:", game.stats.score_blue
    score = score + game.stats.score_blue
    ammo += game.stats.ammo_blue
    enemyammo += game.stats.ammo_red
    kills += game.stats.deaths_red
    deaths += game.stats.deaths_blue
    thinktime += game.stats.think_time_blue
    steps += game.stats.steps
print "Win Ratio:", score/i, "%"
print "Average Kills:", kills/i
print "Average Deaths:", deaths/i
print "Average Ammo:", ammo/i
print "Average Enemy Ammo:", enemyammo/i
print "Average Think Time:", thinktime/i
print "Average Game Steps:", steps/i
    #print game.stats
    #print game.stats.score_blue








#ammo_amount=2,spawn_time=10,ammo_rate=14,max_see=70,max_turn=math.pi/4,max_score=100
# Will run the entire game.

