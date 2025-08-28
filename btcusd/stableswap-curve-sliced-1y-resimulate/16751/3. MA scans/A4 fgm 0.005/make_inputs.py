#!/usr/bin/env python3

import numpy as np
from math import log10
import json
import itertools
from copy import copy


X = np.logspace(log10(200), log10(30000), 64)
Xname = "ma_half_time"
Y = np.logspace(log10(0.002), log10(0.15), 64)
Yname = "boost_rate"

pow = 1.5
fee_gamma_mul = 0.005 / 4 ** pow  # fee_gamma = fee_gamma_mul * A

other_params = dict(
    D=20e6,
    adjustment_step=1e-7,
    fee_gamma=0.001,
    ma_half_time=600,
    out_fee=0.025,
    mid_fee=0.005,
    gas_fee=1,
    n=2,
    log=0,
    allowed_extra_profit=1e-10,
    ext_fee=0.00015,
    gamma=0,
    boost_rate=0.05,
    A=4)

config = {
    'configuration': [],
    'datafile': ["train-1y-1675126920-btcusd"],
    'debug': 0}

for x, y in itertools.product(X, Y):
    params = copy(other_params)
    params[Xname] = x
    params[Yname] = y
    params["fee_gamma"] = fee_gamma_mul * params['A'] ** pow
    config['configuration'].append(params)

with open('configuration.json', 'w') as f:
    json.dump(config, f)
