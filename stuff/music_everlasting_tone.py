# for generating the everlasting tone music

from time import sleep

max_vel = 60
dur = 400
wind_down = 300
oct_span = 7
concurrent_notes = 6

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
        print(t)
        # could arpegiate!
        for nn in range(concurrent_notes):
            c.noteon(t[0][c], t[1][c])
        sleep(0.05)
        for nn in range(concurrent_notes):
            c.noteoff(t[0][c])

