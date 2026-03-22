# Analysis and improvements of YB pools

## Performance of existing pools and room for improvement

Yield Basis uses Curve Twocrypto pools with stableswap invariant under the hood. These pools are characterized by multiple parameters (peak liquidity concentration `A` called amplification factor, dynamic fees characterized by `min_fee`, `max_fee`, `fee_gamma`), and "refuel rate" coming from Yield Basis to the pools. The performance of the pool can be characterized with growth of its value (given as `virtual price`) - and that value corresponds to pool's value when it is balanced and how well `price_scale` - the price around which liquidity is centered - follows the real price.

Brief summary of the research can be seen in one picture:
![](combined/before-and-after.png)

Data for this research can be found [on yb-simulations GitHub](https://github.com/yield-basis/yb-simulations/tree/master/btcusd/lpf%20vs%20old).

### Following `price_scale`

Starting from the middle of November, here is how `price_scale` for cbBTC pool as an example appears to follow the real prices:
![cbBTC price_scale](./real_cbbtc/real-cbbtc-pool-ps.png)

You can see that `price_scale` followed real prices for some time, and then deviated.

And here is what you can see if we try to simulate the behavior of the pool for exactly the same timeframe with exactly the same parameters:
![BTC price_scale short simulation](old_short/prices-sim-old-zoom.png)

Simulations under-estimate performance of the pool slightly. This is fair because simulations ONLY account for arbitrage between pool and centralized exchanges and totally ignore any extra natural flow through the pools. Biggest extra revenue contributor in real pool in comparison with simulations is transactions involving liquidations in lending platforms. Due to those, pool earns slightly more than we simulated, and real performance is somewhat better.

Let's zoom simulations out to check the range from start of 2025 till now:
![BTC price_scale simulation from 2025](old_short/prices-sim-old.png)

You can see that volatility from the start of 2025 was probably lower than it become later, so `price_scale` was following the real prices nicely until late February 2026.

Let's zoom out even more and see from the start of 2024:
![BTC price_scale simulation from 2024](old/prices-sim-old-full.png)

In 2024, performance of these parameters (due to a much higher short-term volatility) would have been not great also. However, we probably ARE in the same regime as before 2025 now! With current parameters optimal for 2025, the durations of "depegs" could be really large (months).

Another notable feature: `price_scale` is changed in large steps. This is undesirable because it leads to sudden leaks of value to arbitrage traders which can be avoided.

### Pool imbalance

Ideally, Curve pool should consist of 50% BTC + 50% crvUSD, e.g. be balanced. It can at times deviate from that, but ideally we should seek to minimize this deviation: this minimizes TRD (temporary redemption discount) and pressure on crvUSD peg. Pool is ideally balanced when `price_scale = current_price`, however it disbalances when they are not equal, and the disbalance is higher when `A` is higher.

This is how balanced BTC pools practically were since November 2025:
![BTC pool imbalances](real_cbbtc/real-imbalances.png)

One can notice that pools went out of balance as much as 22%/78% in peak when `price_scale` deviated from current price now while the ideal "pegged" balance is 50%/50%.

Let's compare that with simulations over the same time period:
![BTC pool imbalances simulation](old_short/imbalance-sim-old-zoom.png)

One can see that pools are even more imbalanced in simulations because `price_scale` catches up with reality faster than in simulations. It is important to compare because we *want* simulations to slightly under-estimate the performance.

Let's zoom out and see how it would have worked if we started in January 2025:
![BTC pool imbalances simulations 2025](old_short/imbalance-sim-old.png)

And if we started in January 2024:
![BTC pool imbalances simulations 2024](old/imbalances-sim-old-full.png)

It's easy to notice that very long durations of "bullish imbalances" would have happened in 2024, making deviations up to 80%/20%, opposite direction to the current peak deviation 22%/78%.

### Deposit growth - fundamental value and redemption value

Measured growth from November 2025 till now for cbBTC pool:
![Measured value change in cbBTC pool](real_cbbtc/real-cbbtc-growth.png)

And over the same time period - simulated. The growth of simulated fundamental value is a bit smaller because simulations do not account for staked/unstaked split.
![Simulated value change (short)](old_short/growth-sim-old-zoom.png)

Temporary redemption discount is the difference between the two lines on the graph. Simulated TRD is a bit higher because the pool rebalances faster in reality.

If we simulate starting at January 2025:
![Simulated value change (2025)](old_short/growth-sim-old.png)

Again, we can see that parameters would have been workable for 2025 but not really after.

Let's simulate strting at earlier time - January 2024:
![Simulated value change (2024)](old/growth-sim-old-full.png)

Here we see that similar TRD would have been happening in the past followed by the full recovery, however after a pretty long time.

### What are we fixing?

We want to fix the following problems most of which we see on the graphs:

- Very big and long-lasting TRD (redemption value drops). People may not want to wait several months when they are going to exit their positons;
- Large and long-lasting pool imbalances: same issue as what causes TRD, they also affect crvUSD peg limiting scaling;
- Pool asjustment of `price_scale` is too abrupt: that creates sudden drops in fundamental value. That is undesired, and also leaks some value to arbitrage traders;
- LevAMM behavior when pool is very imbalanced: we should always allow trades towards a smaller imbalance (not included on the graphs);
- Curve pools currently can only use 50% fees earned towards rebalancing. Making this fraction tunable appears to make a large difference, as we will see further.