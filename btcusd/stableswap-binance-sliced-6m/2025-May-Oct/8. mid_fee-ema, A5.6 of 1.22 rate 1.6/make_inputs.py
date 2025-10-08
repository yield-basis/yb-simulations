#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.001), log10(0.0122), 64)
Xname = "mid_fee"
Y = np.logspace(log10(400), log10(10000), 64)
Yname = "ma_half_time"

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=0.00198,
    ma_half_time=600,
    mid_fee=0.00143,
    out_fee=0.0122,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.00005,
    gamma=0,
    boost_rate=0.016,
    A=5.2)

config = {
    'configuration': [],
    'datafile': ["btcusdt-may-oct-2025"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
