#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.005), log10(0.07), 100)
Xname = "boost_rate"
Y = np.logspace(log10(5e-5), log10(0.1), 100)
Yname = "fee_gamma"

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=0.003,
    ma_half_time=600,
    mid_fee=0.004,
    out_fee=0.019,
    gas_fee=0,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.0002,
    gamma=0,
    boost_rate=0.035,
    A=3)

config = {
    'configuration': [],
    'datafile': ["btcusdt-2024-J2026"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
