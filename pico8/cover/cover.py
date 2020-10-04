
src_ = 'pico8breed.p8.png'
cover_ = 'cover.png'
cover2_ = 'cover2.png'
target_ = 'pico8breed-cover.p8.png'
# target_ = 'pico8breed-cover2bit.p8.png'

#1 copy
with open(src_, 'rb') as src:
    with open(target_, 'wb') as dst:
        dst.write( src.read() )
        


import os
import random #for add noice
from PIL import Image

cover = Image.open(cover_)
dst = Image.open(target_)
if not cover: raise Exception("Unable to load pico8 cover")
if not dst: raise Exception("Unable to load pico8 cart")


x1,y1, x2,y2 = 15,23, 144,152
dy3,dy4 = 163,183
cy3,cy4 = 153,173
# dsts = dst.load()
# covers = cover.load()
# extract from pixels LSBs
(width, height) = dst.size

# TITLES
def nondata(arr):
    return [d & 0xfc for d in arr]

p = dst.getpixel((x1, dy3))
grey = nondata(p) # grey background

# for y in range(dy3):
#     for x in range(0, width):
#         if x1 < x < x2:
#             cover.putpixel((x, y), p)

# red
# for x in range(x1+1, width):
#     cover.putpixel((x, dy3), (255,0,0,255))

black = (0,0,0,255)
for y in range(20, 0, -1):
    for x in range(0, width):
        if x1 < x < x2:
            # save to cover, temporarly, discarded later
            p = dst.getpixel((x, dy3 + y))
            # print(p, 'grey:', grey)
            if nondata(p) == grey:
                continue            
            cover.putpixel((x, cy3 + y), p) # white text
            # cover.putpixel((x, cy3 + y), black) # black text

# BEVELS
for y in range(0, height):
    for x in range(0, width):
        if x1 < x < x2 and y1 < y < y2:
            continue
        p = dst.getpixel((x, y))
        c = cover.getpixel((x, y))
        new = [0] * 4
        noice = random.randint(0, 3) << 2
        for i in range(4):
            new[i] = (c[i] & 0xfc) |  (p[i] & 0x03)     #2bit
            # new[i] = (c[i] & 0xf8) |  (p[i] & 0x07)     #3bit
            # new[i] = (c[i] & 0xF0) |  (p[i] & 0x02) | 0x0c     #4bit
            # new[i] = (c[i] & 0xF0) |  (p[i] & 0x02) | noice     #4bit+noice
            
        dst.putpixel((x,y), tuple(new))

dst.save(target_)
# cover.save(cover2_)
# dst.show()