#!/usr/bin/env python3

import json
import lzma

import numpy as np

STEP_SIZE = 30 * 86400
SLICE_SIZE = 6 * 30 * 86400

with lzma.open('btcusdt-processed.json.xz', 'r') as f:
    price_data = json.load(f)

min_ts = price_data[0][0]
max_ts = price_data[-1][0]

if max_ts > 1e10:
    STEP_SIZE *= 1000
    SLICE_SIZE *= 1000

ix = np.arange(len(price_data))
ts = np.array([p[0] for p in price_data])

for t in np.arange(min_ts, max_ts - (STEP_SIZE + SLICE_SIZE), STEP_SIZE):
    ixs_train = ix[(ts >= t) * (ts < t + SLICE_SIZE)]
    ixs_verify = ix[(ts >= t + SLICE_SIZE) * (ts < t + SLICE_SIZE + STEP_SIZE)]
    subdata_train = price_data[int(ixs_train.min()):int(ixs_train.max()) + 1]
    subdata_verify = price_data[int(ixs_verify.min()):int(ixs_verify.max()) + 1]

    name_train = f'train-b-{t}-btcusd.json'
    name_verify = f'verify-b-{t}-btcusd.json'
    with open(name_train, 'w') as f:
        json.dump(subdata_train, f)
    with open(name_verify, 'w') as f:
        json.dump(subdata_verify, f)
