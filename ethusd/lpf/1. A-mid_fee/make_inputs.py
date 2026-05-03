#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(1), log10(20), 100)
Xname = "A"
Y = np.logspace(log10(5e-4), log10(0.1), 100)
Yname = "mid_fee"

other_params = dict(
    D=20e6,
    adjustment_step=5e-3,
    fee_gamma=0.003,
    ma_half_time=600,
    mid_fee=0.003,
    out_fee=0.003,
    gas_fee=0,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.0002,
    gamma=0,
    boost_rate=0.035,
    lp_profit_fraction=0.4,
    boost_mul=1,
    boost_min=0,
    A=10)

config = {
    'configuration': [],
    'datafile': ["ethusdt-2024-May2026"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    params['out_fee'] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
