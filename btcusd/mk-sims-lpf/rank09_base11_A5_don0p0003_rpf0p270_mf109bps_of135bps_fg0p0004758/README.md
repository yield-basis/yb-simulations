# Legacy YB Releverage Candidate Output

Candidate ordinal: `6`
Source base index: `11`
Rank by apy_net: `9`
Table params: A=5, donation_apy=0.0003, reserved_profit=0.270, mid_fee_bps=109, out_fee_bps=135, fee_gamma=0.000475794

Rows: `2,171,280`

Files:

- `detailed-output.json.xz`: full-step compressed JSON for the legacy releverage scripts
- `pool_config.json`: one-pool harness config
- `simulate-one.py`, `simulate-optimize.py`: copied legacy releverage scripts patched to load plain JSON

Run from this folder:

```bash
env UV_CACHE_DIR=/tmp/uv-cache MPLBACKEND=Agg uv run --project /Users/michael/Documents/projects/cpp-twocrypto-modular/python python simulate-one.py
```
