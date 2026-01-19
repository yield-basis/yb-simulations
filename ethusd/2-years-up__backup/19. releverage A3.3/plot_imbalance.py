#!/usr/bin/env python3

import pylab
import json
import lzma

import numpy as np


STEP = 500


with lzma.open('detailed-output.json.xz', 'r') as f:
    data = json.load(f)


data = data[::STEP]
t = np.array([d['t'] for d in data])
p = np.array([d['close'] for d in data])
usd = np.array([d['token0'] for d in data])
coin = np.array([d['token1'] for d in data])

usd_f = usd / (usd + coin * p)
days = (t - t[0]) / 86400

pylab.plot(days, usd_f, c="black")
pylab.tight_layout()
pylab.show()
