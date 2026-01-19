#!/usr/bin/env python3

import pylab
import json
import lzma


STEP = 500


with lzma.open('detailed-output.json.xz', 'r') as f:
    data = json.load(f)


data = data[::STEP]
t = [d['t'] for d in data]
p = [d['close'] for d in data]
ps = [d['price_scale'] for d in data]

pylab.plot(t, p, c="black")
pylab.plot(t, ps, c="gray")
pylab.tight_layout()
pylab.show()
