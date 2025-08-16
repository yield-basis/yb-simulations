#!/usr/bin/env python3

import json
import os


summary_files = sorted(os.listdir('verify-summary'))

FEE = 1e-4
yb_growth = 1.4454
total_time = 0
total_specific_volume = 0

for i, name in enumerate(summary_files):
    with open('verify-summary/' + name, 'r') as f:
        data = json.load(f)
        if i == 0:
            total_time += 365
        else:
            total_time += 30
        total_specific_volume += float(data['configuration'][0]['Result']['volume'])

annual_volume = total_specific_volume * 365 / total_time
returns_per_tvl = 2 * annual_volume * FEE
apr = (yb_growth ** (1 / total_time) - 1) * 365


print(f'Total time: {total_time} days')
print(f'Total specific volume: {total_specific_volume:.2f}')
print(f'Average annual volume: {annual_volume:.2f}')
print(f'Annual returns per TVL: {returns_per_tvl*100:.2f}%')
print(f'Average YB APR in the observed time: {apr*100:.2f}%')
