from PIL import Image, ImageDraw
import random
import json
import os
import math
import time

WORKSIZE = 64

target = Image.open("target1.png")
# target2 = target2.resize((WORKSIZE, WORKSIZE), resample=Image.LANCZOS)
# target2.save("temp/target.png")
# target = Image.new(mode="RGBA", size=(WORKSIZE, WORKSIZE))
# target.paste(target2, (0,0))

lastlayer = Image.new(mode="RGB", size=(WORKSIZE, WORKSIZE))
draw = ImageDraw.Draw(lastlayer)
draw.rectangle([(0, 0), lastlayer.size], fill=(255,255,255,255))
del draw

def rendercandidate(candidate, lastlayer):
    temp2 = Image.new(mode="RGB", size=(WORKSIZE, WORKSIZE))
    temp = Image.new(mode="RGBA", size=(WORKSIZE, WORKSIZE))
    draw = ImageDraw.Draw(temp)
    draw.rectangle([(0, 0), temp.size], fill=(255,255,255,255))
    del draw
    overlay = Image.new(mode="RGBA", size=(WORKSIZE, WORKSIZE))
    draw = ImageDraw.Draw(overlay)
    # draw.rectangle([(0, 0), lastlayer.size], fill=(0,0,0,0))
    # draw.line((0, 0) + overlay.size, fill=WORKSIZE)
    draw.ellipse(candidate['corners'], fill = candidate['color'])
    # draw.polygon(candidate['corners'], fill = candidate['color'])
    del draw
    temp.paste(lastlayer, (0, 0))
    temp.alpha_composite(overlay, (0, 0))
    temp2.paste(temp, (0, 0))
    # return temp
    return temp2

def scorecandidate(candidateimage, targetimage):
    ic = candidateimage.tobytes()
    it = targetimage.tobytes()
    # print("ic=%d, it=%d" % (len(ic), len(it)))
    diff = 0
    np = len(ic)
    for k in range(0, np):
        dr = abs(ic[k] - it[k])
        diff += dr*dr
    diff /= np
    return diff

PALETTE = [
    # (0x00, 0x00, 0x00),

    # (0xFF, 0x00, 0x00),
    # (0x00, 0xFF, 0x00),
    # (0x00, 0x00, 0xFF),

    # (0xaa, 0xa1, 0xbd),
    # (0x9c, 0x99, 0xa9),
    # (0x84, 0x58, 0x40),
    # (0x9a, 0x6c, 0x66),
    # (0x2e, 0x2c, 0x23),
    # (0x69, 0x62, 0x5f),

    (0xff, 0xa1, 0x95),
    (0x21, 0x19, 0x04),
    (0xe9, 0xa6, 0xc8),
    (0x5f, 0x23, 0x00),
    (0xFF, 0xFF, 0xFF),
]
lastmillis = int(round(time.time() * 1000))
ms_per_frame = 10000

all_best = []
for phase in range(0, 100):

    if os.path.exists('temp/p' + str(phase) + '.png'):
        print ("Skipping phase %d" % (phase))
        target2 = Image.open('temp/p' + str(phase) + '.png')
        lastlayer.paste(target2)
        continue

    bestcandidate = None
    bestimage = None

    millis = int(round(time.time() * 1000))
    ms_per_frame = (ms_per_frame + (millis - lastmillis)) / 2
    fps = 1000.0 / ms_per_frame

    for k in range(0, 255):
        gs = math.floor(64 / 10)
        hs = 32
        rr = (k / 10) % 30
        # aa = k * math.pi / 30
        xi = random.randint(0, 15) # hs + rr * math.cos(aa)
        yi = random.randint(0, 15) # hs + rr * math.sin(aa)
        pn = yi * 16 + xi
        xc = xi * 4 # hs + rr * math.cos(aa)
        yc = yi * 4 # hs + rr * math.sin(aa)
        # xc = gs * random.randint(0, 10)
        # yc = gs * random.randint(0, 10)
        rr = (math.floor(k / 8) % 8) * 2
        ci = k % len(PALETTE)
        cr = PALETTE[ci][0]
        cg = PALETTE[ci][1]
        cb = PALETTE[ci][2]
        candidate = {
            'index': k,
            'radius': rr,
            'positionindex': pn,
            'colorindex': ci,
            'center': [xc, yc],
            'corners': [
                (xc - rr, yc - rr), # random.randint(0, WORKSIZE), random.randint(0, WORKSIZE)),
                (xc + rr, yc + rr), # (random.randint(0, WORKSIZE), random.randint(0, WORKSIZE)),
            ],
            'color': (cr, cg, cb, 64),
            'score': 0,
        }

        temp = rendercandidate(candidate, lastlayer)
        candidate['score'] = scorecandidate(temp, target)

        if k % 50 == 0:
            print('attempt %d... (%f ms per frame, %f fps)\r' % (k, ms_per_frame, fps), end='')
        if bestcandidate == None or candidate['score'] < bestcandidate['score']:
            print ("phase %d, iter %d, score %d, triangle %r" % (phase, k, candidate['score'], candidate['corners']))
            # print ("found best candidate.")
            bestcandidate = candidate
            bestimage = temp
            # temp.save("temp/p" + str(phase) + "-i" + str(k) + "-diff" + str(candidate["score"])+ ".png")

        # temp.save("temp/p" + str(phase) + "-i" + str(k) + ".png")

        del temp
        lastmillis = millis

    print ("after phase %d, best candidate %r" % (phase, bestcandidate))

    newlayer = rendercandidate(bestcandidate, lastlayer)
    del lastlayer
    lastlayer = newlayer
    lastlayer.save('temp/p' + str(phase) + '.png')
    all_best.append(bestcandidate)

    with open('temp2/p' + str(phase) + '.json', 'w') as f:
        json.dump(bestcandidate, f)

with open('temp2/all.json', 'w') as f:
    json.dump(all_best, f, indent=4, separators=(',', ': '))
