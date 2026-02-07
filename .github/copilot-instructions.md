# Copilot / AI agent instructions — DoFManager

Quick, focused instructions to help an AI coding agent be productive in this repository.

Overview
- Purpose: small Football Manager–like simulator (CLI + Tkinter GUI). Key runtime artifacts: the SQLite DB `futbol_manager.db` and optional save `partida.json`.
- Main entry points: `main.py` (CLI flow) and `gui.py` (Tkinter app). Simulation logic lives in `match_engine.py` and domain models in `potencial.py`.

Architecture & data flow (high level)
- `gui.py`: Tk UI, loads teams from SQLite via `database.py` and fills `EquipoReal` objects, uses `Liga` to manage fixtures and standings, and calls `match_engine.simular_partido_mejorado()` to run matches and produce a chronology (list of strings) shown in the UI.
- `main.py`: simple CLI runner that can create a world (`nueva_partida()`), run game loop and call the same `match_engine` functions. Use this for headless runs.
- `potencial.py`: canonical `Jugador` class (states, `ca`, `pa`, training/recuperación). When changing player fields, update all loaders that construct instances from DB (see `gui.py:EquipoReal.cargar_plantilla_desde_db`).
- `liga.py`: holds competition state, `tabla`, `calendario`, save/load to `partida.json`.
- `atributos.py` + `generar_jugadores.py`: helper generators for attributes, free agents, and scripts to bulk-populate `jugadores` in the DB.
- `database.py`: creates `equipos` table and default teams. DB schema is the single source of truth for persistent storage.

Important files to inspect when changing behavior
- UI / flow: [gui.py](gui.py) (UI + `EquipoReal` used by GUI)
- CLI: [main.py](main.py)
- Match logic: [match_engine.py](match_engine.py)
- Domain model: [potencial.py](potencial.py)
- League state & persistence: [liga.py](liga.py)
- DB schema / init: [database.py](database.py)
- Data generators: [generar_jugadores.py](generar_jugadores.py), [atributos.py](atributos.py)

Project-specific conventions & gotchas
- Language & strings: project uses Spanish strings and emojis in output; preserve tone for UX consistency.
- Scales: player `ca` / `pa` use an internal 0–200 scale in `potencial.py` (and UIs assume CA/PA numeric ranges). Many calculations derive `nivel_medio` as `ca / 2` or similar — changing scale requires touching `liga.py`, `gui.py` and `match_engine.py`.
- Duplicate/overlapping models: lightweight `EquipoReal` appears both in `main.py` and `gui.py` with slightly different fields (DB `id_db`, `presupuesto`, `entrenador` present in GUI). Prefer `potencial.py` for `Jugador` and `liga.py` for league logic when adding canonical behavior.
- Persistence: DB file name is `futbol_manager.db`. `database.py` creates `equipos` table and default rows; `generar_jugadores.py` inserts into `jugadores` table (script clears `jugadores` before reinserting).
- Save format: `liga.guardar_partida()` writes JSON to `partida.json` with `tabla`, `calendario`, `jornada_actual` — keep compatibility when changing `Liga` fields.

Developer workflows / common commands
- Initialize DB (creates `equipos`):
```
python database.py
```
- Populate players into DB (run after DB init):
```
python generar_jugadores.py
```
- Run GUI (recommended for manual testing):
```
python gui.py
```
- Run CLI runner (headless flow + simple menu):
```
python main.py
```

Integration & extension tips
- When adding a DB column: (1) update `database.py` schema, (2) update `generar_jugadores.py` insertion, (3) update `gui.py:EquipoReal.cargar_plantilla_desde_db` to map DB fields into `Jugador` constructor.
- When changing `Jugador` internals (e.g., rename `ca` or `pa`): update all loaders (`gui.py`, `main.py`) and any code that references `jugador.ca` (match_engine, liga, mercado logic).
- Match output: `simular_partido_mejorado()` returns a `cronica` list; UI appends each string to the results text box. For structured events consider returning dicts but ensure UI code adapts.

Style & safety
- No type hints or tests in repo — prefer minimal, backwards-compatible changes.
- Keep prints/emojis and Spanish messages unless explicitly asked to internationalize.

If you change major structures
- Add migration notes in `README.md` explaining required manual DB migration steps.
- Update `gui.py` and `main.py` to preserve backwards-compatible loading of older `partida.json` and DB rows.

Questions for the maintainer
- Which `EquipoReal` implementation should be canonical (the one in `gui.py` has DB integration)?
- Do you want to standardize `Entrenador` into a single file (duplicate small definitions exist)?

---
If this draft misses any repo-specific flows (CI, external services), tell me what to add and I'll iterate.
