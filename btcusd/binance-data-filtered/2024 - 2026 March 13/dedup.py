#!/usr/bin/env python3

import json
import lzma
import sys

with lzma.open(sys.argv[1]) as f:
    data = json.load(f)

ddata = {}
for d in data:
    if d[0] not in ddata:
        ddata[d[0]] = d

out = []
for t in sorted(ddata.keys()):
    out.append(ddata[t])

with open(sys.argv[1].split('.')[0] + '.json', 'w') as f:
    json.dump(out, f)
