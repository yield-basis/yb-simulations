#!/usr/bin/env python3

import pylab
import json
import lzma

import numpy as np
from datetime import datetime


STEP = 500


with lzma.open('detailed-output.json.xz', 'r') as f:
    data = json.load(f)

t = np.array([d['t'] for d in data])
vp = np.array([(d['xcp'] + 1) / 2 for d in data])
ri = np.array([d['boost_rate'] for d in data])
ri = 1 + np.array([0] + list(np.cumsum(ri[:-1] * (t[1:] - t[:-1]))))

t = [datetime.fromtimestamp(_t) for _t in t[::STEP]]
vp = vp[::STEP] / ri[::STEP]

pylab.plot(t, vp, c="black")
pylab.xlabel('Time')
pylab.ylabel('vp - rate')
pylab.xticks(rotation=45, ha='right')
pylab.grid()
pylab.tight_layout()
pylab.show()
