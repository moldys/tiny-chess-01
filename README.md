# tiny-chess-01 entry

Negamax / alpha-beta chess engine in <= 4096 bytes of Python (self-extracting
zlib payload in `main.py`). Deterministic, standard-library only, speaks the
make.fun tiny-chess-01 env protocol over HTTP (JSON).

Run: `MAKEFUN_ENV_URL=<env> python3 -P -s main.py`
Tuning env vars: `ENGINE_BUDGET` (node cap per move) and `ENGINE_DEPTH`.
