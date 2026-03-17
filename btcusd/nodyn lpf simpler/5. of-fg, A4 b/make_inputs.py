#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.0051), log10(0.045), 100)
Xname = "out_fee"
Y = np.logspace(log10(3e-4), log10(3e-2), 100)
Yname = "fee_gamma"

other_params = dict(
    D=20e6,
    adjustment_step=5e-3,
    fee_gamma=0.00394,
    ma_half_time=600,
    mid_fee=0.00542,
    out_fee=0.0131,
    gas_fee=0,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.0002,
    gamma=0,
    boost_rate=0.01405,
    A=4,
    lp_profit_fraction=0.445,
    boost_mul=1,
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
