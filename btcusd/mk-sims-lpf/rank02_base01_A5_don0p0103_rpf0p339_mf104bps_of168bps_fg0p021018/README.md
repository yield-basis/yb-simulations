# Legacy YB Releverage Candidate Output

Candidate ordinal: `1`
Source base index: `1`
Rank by apy_net: `2`
Table params: A=5, donation_apy=0.0103, reserved_profit=0.339, mid_fee_bps=104, out_fee_bps=168, fee_gamma=0.0210175

Rows: `2,171,280`

Files:

- `detailed-output.json.xz`: full-step compressed JSON for the legacy releverage scripts
- `pool_config.json`: one-pool harness config
- `simulate-one.py`, `simulate-optimize.py`: copied legacy releverage scripts patched to load plain JSON

Run from this folder:

```bash
env UV_CACHE_DIR=/tmp/uv-cache MPLBACKEND=Agg uv run --project /Users/michael/Documents/projects/cpp-twocrypto-modular/python python simulate-one.py
```
