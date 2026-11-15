# tiny-chess-01 entry
[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/moldys/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/moldys/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Bounty page: [https://make.fun/bounty/tiny-chess-01](https://make.fun/bounty/tiny-chess-01)

Negamax / alpha-beta chess engine in <= 4096 bytes of Python (self-extracting
zlib payload in `main.py`). Deterministic, standard-library only, speaks the
make.fun tiny-chess-01 env protocol over HTTP (JSON).

Run: `MAKEFUN_ENV_URL=<env> python3 -P -s main.py`
Tuning env vars: `ENGINE_BUDGET` (node cap per move) and `ENGINE_DEPTH`.
