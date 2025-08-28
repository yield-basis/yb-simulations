#!/usr/bin/env python3

import pylab
import numpy as np

f0 = 0.1


s = np.linspace(0, 1, 1000)
k = s * (1 - f0) / (np.sqrt(1 - s) * (1 - (1 - f0) * np.sqrt(1 - s)))

pylab.plot(k, s)
pylab.xlabel('k')
pylab.ylabel('s')
pylab.xlim(0, 5)
pylab.ylim(0, 1)
pylab.tight_layout()
pylab.show()
