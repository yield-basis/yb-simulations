#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(200), log10(20000), 64)
Xname = "ma_half_time"
Y = np.logspace(log10(0.005), log10(0.09), 64)
Yname = "boost_rate"

pow = 1.5
fee_gamma_mul = 0.0408 / 8.2 ** pow  # fee_gamma = fee_gamma_mul * A

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=0.001,
    ma_half_time=1220,
    out_fee=0.025,
    mid_fee=0.004,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.00015,
    gamma=0,
    boost_rate=0.035,
    A=7.5)

config = {
    'configuration': [],
    'datafile': ["train-1y-1695862920-btcusd"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    params["fee_gamma"] = fee_gamma_mul * params['A'] ** pow
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
