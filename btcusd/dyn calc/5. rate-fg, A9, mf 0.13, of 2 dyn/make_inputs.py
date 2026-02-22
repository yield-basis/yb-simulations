#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.01), log10(5), 100)
Xname = "boost_rate"
Y = np.logspace(log10(1e-8), log10(1), 100)
Yname = "fee_gamma"

other_params = dict(
    D=20e6,
    adjustment_step=5e-3,
    fee_gamma=0.003,
    ma_half_time=600,
    mid_fee=0.0013,
    out_fee=0.02,
    gas_fee=0,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.0002,
    gamma=0,
    boost_rate=0.035,
    A=9,
    boost_mul=0,
    boost_min=0)

config = {
    'configuration': [],
    'datafile': ["btcusdt-2024-F2026"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
