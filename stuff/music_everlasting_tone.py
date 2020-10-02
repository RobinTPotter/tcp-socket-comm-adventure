# for generating the everlasting tone music

from time import sleep
TRANS = 12
SLEEP = 0.005
SLEEP_INT = 0.2
max_vel = 20
dur = 400
wind_down = 300
oct_span = 6
concurrent_notes = 4

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

for t in ticks:
    print(t)
# play beautiful music

def play(c):
    for t in ticks:
        #print(t)
        # could arpegiate!
        for nn in range(concurrent_notes):
            c.note_on(TRANS+t[0][nn], t[1][nn])
            sleep(SLEEP)
        for nn in range(concurrent_notes):
            c.note_off(TRANS+t[0][nn])
        sleep(SLEEP_INT)

import pygame.midi as pm
pm.init()
for c in [c for c in range(pm.get_count()) if pm.get_device_info(c)[3]==1]:
    print(str(pm.get_device_info(c)[1]).lower(), pm.get_device_info(c))

desc = 'u2midi'
device_num = [c for c in range(pm.get_count()) if desc.lower() in str(pm.get_device_info(c)[1]).lower() and pm.get_device_info(c)[3]==1][0]
device = pm.Output(device_num)

play(device)
