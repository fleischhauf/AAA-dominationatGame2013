from domination import core
import math
import time
'''
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ C _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ a _ _ _ _ _ _ _ _ _ _ w
w R _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ B w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ B w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ B w
w _ _ _ _ _ _ _ _ _ _ a _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ C _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
'''
FIELD = """
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ C _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ w w w w w w w w w w w w w w w _ _ _ _ _ _ _ w
w _ _ _ w _ _ _ w _ _ _ _ _ _ _ _ _ _ a _ _ _ _ _ _ w _ _ _ w
w R _ _ w _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ B w
w R _ _ w _ _ _ w _ _ _ _ w w w w w _ _ _ _ w _ _ _ w _ _ B w
w R _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ w _ _ B w
w _ _ _ w _ _ _ _ _ _ a _ _ _ _ _ _ _ _ _ _ w _ _ _ w _ _ _ w
w _ _ _ _ _ _ _ w w w w w w w w w w w w w w w _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ C _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
"""

#These are the oficial settings
#settings = core.Settings(max_turn=0, think_time=0.059999999999999998, ammo_rate=9, spawn_time=11, ammo_amount=1, max_steps=300, max_score=100, max_see=80)
settings = core.Settings(max_turn=0.78539816339744828, think_time=0.059999999999999998, ammo_rate=9, spawn_time=11, ammo_amount=1, max_steps=300, max_score=100, max_see=80)
FI = core.Field.from_string(FIELD)
f = open("outcome_wolf_single_standard_agent.csv","w")
score = 0
ammo = 0
enemyammo = 0
kills = 0
deaths = 0
thinktime = 0
steps = 0
steps_mov = [0,0,0,0,0,0,0,0,0,0]
f.write("game,score,steps,steps_avrg,kills,deaths,ammo,enemy_ammo,think_time\n")

for i in range(0, 1000):
    
    #red_init={'blob': open('stateActionValues.p','rb')}
    old_time = time.time()
    #if(i % 1 == 2000):
    #    game = core.Game('domination/agent.py', 'domination/sillybot.py',blue_init={'blob': open('tmemory.p','rb')},#wolf-tables-joint-action
    #                 record=False, rendered=True,verbose=True, settings=settings, field=FI)
    #else:
        
    game = core.Game('domination/agent.py', 'domination/wolf_single.py',blue_init={'blob': open('wolf-tables_single.p','rb')},
                    record=False, rendered=False,verbose=False, settings=settings, field=FI)
        
    game.run()
    #print game.stats
    #print("time taken:",time.time()-old_time)
    steps_mov.pop(0)
    steps_mov.append(game.stats.steps)    
    steps_total = 0
    for j in steps_mov:
        steps_total += j
    
    steps_avrg = steps_total/len(steps_mov)
    score =  game.stats.score_blue
    ammo = game.stats.ammo_blue
    enemyammo = game.stats.ammo_red
    kills = game.stats.deaths_red
    deaths = game.stats.deaths_blue
    thinktime = game.stats.think_time_blue
    steps = game.stats.steps
    
    print "Game:", i, "| Score:", game.stats.score_blue,"| steps:",game.stats.steps,"| avrg_steps:",steps_avrg
    f.write(str(i)+","+str(score)+","+str(steps)+","+str(steps_avrg)+","+str(kills)+","+str(deaths)+","+str(ammo)+","+str(enemyammo)+","+str(thinktime)+"\n")
    #if(game.stats.score_red > 90):
    #    break
    #score = score + game.stats.score_blue
    #ammo += game.stats.ammo_blue
    #enemyammo += game.stats.ammo_red
    #kills += game.stats.deaths_red
    #deaths += game.stats.deaths_blue
    #thinktime += game.stats.think_time_blue
    #steps += game.stats.steps
print "Win Ratio:", score/i, "%"
print "Average Kills:", kills/i
print "Average Deaths:", deaths/i
print "Average Ammo:", ammo/i
print "Average Enemy Ammo:", enemyammo/i
print "Average Think Time:", thinktime/i
print "Average Game Steps:", steps/i
