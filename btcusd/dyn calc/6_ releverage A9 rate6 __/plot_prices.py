#!/usr/bin/env python3

import pylab
import json
import lzma

from datetime import datetime


STEP = 500


with lzma.open('detailed-output.json.xz', 'r') as f:
    data = json.load(f)


data = data[::STEP]
t = [datetime.fromtimestamp(d['t']) for d in data]
p = [d['close'] for d in data]
ps = [d['price_scale'] for d in data]

pylab.plot(t, p, c="black", label="Spot price")
pylab.plot(t, ps, c="gray", label="price_scale")
pylab.xlabel('Time')
pylab.ylabel('Price')
pylab.xticks(rotation=45, ha='right')
pylab.legend()
pylab.grid()
pylab.tight_layout()
pylab.show()
