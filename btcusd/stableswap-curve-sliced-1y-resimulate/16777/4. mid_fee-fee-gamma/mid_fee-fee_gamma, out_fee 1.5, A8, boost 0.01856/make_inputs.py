#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.0005), log10(0.025), 64)
Xname = "mid_fee"
Y = np.logspace(log10(1e-7), log10(1), 64)
Yname = "fee_gamma"

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=2.26e-6,
    ma_half_time=600,
    mid_fee=0.008,
    out_fee=0.015,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.00015,
    gamma=0,
    boost_rate=0.0187,
    A=8)

config = {
    'configuration': [],
    'datafile': ["train-1y-1677718920-btcusd"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
