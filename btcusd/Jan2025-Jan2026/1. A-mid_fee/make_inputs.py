#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(2), log10(50), 100)
Xname = "A"
Y = np.logspace(log10(10e-4), log10(0.1), 100)
Yname = "mid_fee"

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=0.003,
    ma_half_time=600,
    mid_fee=0.003,
    out_fee=0.003,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.0004,
    gamma=0,
    boost_rate=0.035,
    A=9)

config = {
    'configuration': [],
    'datafile': ["btcusdt-J2025-J2026"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    params['out_fee'] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
