#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(0.02), log10(0.25), 100)
Xname = "boost_rate"
Y = np.logspace(log10(1e-6), log10(0.5), 100)
Yname = "fee_gamma"

other_params = dict(
    D=20e6,
    adjustment_step=5e-3,
    fee_gamma=0.003,
    ma_half_time=600,
    mid_fee=0.007,
    out_fee=0.022,
    gas_fee=0,
    n=2,
    log=0,
    allowed_extra_profit=1e-12,
    ext_fee=0.0001,
    gamma=0,
    boost_rate=0.045,
    A=5)

config = {
    'configuration': [],
    'datafile': ["ethusdt-2yup"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
