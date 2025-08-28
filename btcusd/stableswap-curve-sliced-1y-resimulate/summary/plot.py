#!/usr/bin/env python3

import pylab
import lzma
import json
import os

import numpy as np
from datetime import datetime

STEP = 100

train_files = sorted(os.listdir('train'))
verify_files = sorted(os.listdir('verify'))

print(f'Loading {train_files[0]}')
with lzma.open('train/' + train_files[0], 'r') as f:
    data = json.load(f)

vp = data[-1]['loss']

for name in verify_files:
    with lzma.open('verify/' + name, 'r') as f:
        print(f'Loading {name}')
        subdata = json.load(f)
        subdata = [{'t': d['t'], 'loss': d['loss'] * vp} for d in subdata]
        data += subdata
        vp = subdata[-1]['loss']

print('Calculating values')
t = [datetime.fromtimestamp(d['t']) for d in data[::STEP]]
vp = np.array([d['loss'] for d in data[::STEP]])
vp = vp * 100 - 100

print('Plotting')
pylab.plot(t, vp)
pylab.xticks(rotation=45, ha='right')
pylab.xlabel('t')
pylab.ylabel('Deposit growth (%)')
pylab.tight_layout()
pylab.show()
