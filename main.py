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

#These are the oficial settings
settings = core.Settings(think_time=0.059999999999999998, ammo_rate=9, ammo_amount=1, max_steps=300, max_score=100, max_see=80, max_turn=0.78539816339744828)
FI = core.Field.from_string(FIELD)
score = 0
ammo = 0
enemyammo = 0
kills = 0
deaths = 0
thinktime = 0
steps = 0

for i in range(1, 4):
    game = core.Game('domination/agent.py', 'domination/superagent.py',
                     record=True, rendered=False,verbose=True, settings=settings, field=FI)
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