import json
import os
from web3mc import Multicall
from datetime import datetime

import asyncio


RPC = "http://127.0.0.1:8545"  # Replace with your node
multicall = Multicall(
    provider_url=RPC,
    batch=30,
    max_retries=3,
    gas_limit=50_000_000,
    _semaphore=1000
)
w3 = multicall.async_web3

START_BLOCK = 16308500
END_BLOCK = 22649000
BATCH = 100

with open('curve.json', 'r') as f:
    abi = json.load(f)

pool = w3.eth.contract('0xD51a44d3FaE010294C616388b506AcdA1bfAAE46', abi=abi)


def batched(iterable, n=1):
    length = len(iterable)
    for ndx in range(0, length, n):
        yield iterable[ndx:min(ndx + n, length)]


async def get_prices(b):
    result = await multicall.async_aggregate([
        pool.functions.get_dy(0, 1, 10**7),
        pool.functions.get_dy(1, 0, 10000)], block_identifier=b)
    return (10**7 / result[0] / 1e6 * 1e8 + result[1] / 10000 / 1e6 * 1e8) / 2


def candle2line(t, candle):
    maxmin = [max(candle), min(candle)]
    if candle.index(maxmin[0]) > candle.index(maxmin[1]):
        maxmin = [maxmin[1], maxmin[0]]
    return [t, candle[0], maxmin[0], maxmin[1], candle[-1], 1e10]


async def main():
    # Format: time, open, high, low, close, vol; vol will be not real
    t_candle = (await w3.eth.get_block(START_BLOCK))['timestamp'] // 60 * 60
    candle_btc = []

    full_btc = []
    used_timestamps = set()

    if os.path.exists('curve-btcusdc-1m.json'):
        with open('curve-btcusdt-1m.json', 'r') as f:
            full_btc = json.load(f)

        for candle in full_btc:
            used_timestamps.add(candle[0])

    for batch in batched(range(START_BLOCK, END_BLOCK + 1), BATCH):
        tasks = []
        for b in batch:
            tasks.append(w3.eth.get_block(b))
            tasks.append(get_prices(b))
        results = await asyncio.gather(*tasks)

        for block, prices in batched(results, 2):
            t = block['timestamp']
            p_btc = prices

            if t // 60 * 60 == t_candle:
                candle_btc.append(p_btc)

            else:
                if len(candle_btc) > 0 and t_candle not in used_timestamps:
                    full_btc.append(candle2line(t_candle, candle_btc))
                candle_btc = []
                t_candle = t // 60 * 60

            if block.number % 1000 == 0 or block.number == END_BLOCK:
                print(f't={datetime.fromtimestamp(t)}, block={block.number}, btc={p_btc}')
                with open('curve-btcusdc-1m.json', 'w') as f:
                    json.dump(full_btc, f)


if __name__ == '__main__':
    asyncio.run(main())
