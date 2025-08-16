#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.002), log10(0.025), 100)
Xname = "mid_fee"
Y = np.logspace(log10(1e-4), log10(1), 100)
Yname = "fee_gamma"

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=2.26e-6,
    ma_half_time=1354,
    mid_fee=0.0041,
    out_fee=0.025,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.00015,
    gamma=0,
    boost_rate=0.034,
    A=8.2)

config = {
    'configuration': [],
    'datafile': ["train-1y-1690678920-btcusd"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
