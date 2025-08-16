Yield Basis simulations
=========================


Cryptopools simulator
-----------------------
/cryptopool-simulator - external link to cryptopool simulator.

Building the simulator which uses stableswap invariant:
```
cd cryptopool-simulator
make simus
```

Running simulations in a single thread:
```
./simus input_file.json out_file.json
```

For running simulations use `N` equal to your total number of cores (virtual AND real) in the following command:
```
./simus threads=N configuration.json results.json
```
