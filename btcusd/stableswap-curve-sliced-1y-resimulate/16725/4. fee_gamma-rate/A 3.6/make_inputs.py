#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(1e-5), log10(1), 64)
Xname = "fee_gamma"
Y = np.logspace(log10(0.001), log10(0.1), 64)
Yname = "boost_rate"

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=0.001,
    ma_half_time=600,
    out_fee=0.03,
    mid_fee=0.00213,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.00015,
    gamma=0,
    boost_rate=0.05,
    A=3.6)

config = {
    'configuration': [],
    'datafile': ["train-1y-1672534920-btcusd"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
