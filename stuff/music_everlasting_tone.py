# for generating the everlasting tone music

from time import sleep
TRANS = 12
SLEEP = 0.05
SLEEP_INT = 0.2
max_vel = 60
dur = 400
wind_down = 300
oct_span = 5
concurrent_notes = 3

ticks = []

for t in range(0,dur):

    notes = [(t + nn * 12)%(oct_span * 12) for nn in range(concurrent_notes)]
    velocities = [int(max_vel * (1-(float(abs((t + nn * 12)%(oct_span * 12) - (oct_span * 12) / 2)))/(oct_span * 12 / 2))) for nn in range(concurrent_notes)]
    #print (( notes , velocities ))
    ticks.append((notes,velocities))

activated = [0 for nn in range(concurrent_notes)]
counter = wind_down

for t in ticks:
    counter -= 1
    for nn in range(concurrent_notes):
        if counter > 0:
            if t[1][nn]==0: activated[nn] = 1
            if activated[nn]==0 and t[1][nn]>0: t[1][nn] = 0
        if counter < 0:
            if t[1][nn]==0: activated[nn] = 0
            if activated[nn]==0 and t[1][nn]>0: t[1][nn] = 0


# play beautiful music

def play(c):
    for t in ticks:
        #print(t)
        # could arpegiate!
        for nn in range(concurrent_notes):
            c.noteon(TRANS+t[0][nn], t[1][nn])
            sleep(SLEEP)
        #for nn in range(concurrent_notes):
        #    c.noteoff(TRANS+t[0][nn])
        sleep(SLEEP_INT)

import pygame.midi as pm
pm.init()
for d in [str(pm.get_device_info(c)[1]).lower() for c in range(pm.get_count()) if pm.get_device_info(c)[3]==1][0]]:
    print(d)
    
desc = 'u2midi'
device_num = [c for c in range(pm.get_count()) if desc.lower() in str(pm.get_device_info(c)[1]).lower() and pm.get_device_info(c)[3]==1][0]
device = pm.Output(device_num)

play(device)
