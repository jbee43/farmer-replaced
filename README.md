# farmer-replaced

Modular automation scripts for [The Farmer Was Replaced](https://thefarmerwasreplaced.com/)

## Modules

| File                  | Description                                            |
| --------------------- | ------------------------------------------------------ |
| **Core**              |                                                        |
| `nav.py`              | Movement: `home()`, `to(x,y)`, `advance()`             |
| `water.py`            | Watering: `ensure(threshold)`                          |
| `sow.py`              | Tile prep: ground type, plant, water in one call       |
| **Farms**             |                                                        |
| `farm_hay.py`         | Grass on grassland                                     |
| `farm_wood.py`        | Tree/bush checkerboard (avoids adjacency slowdown)     |
| `farm_carrot.py`      | Carrots on soil with water                             |
| `farm_pumpkin.py`     | Mega-pumpkin cascade (yield = count^3) with fertilizer |
| `farm_sunflower.py`   | Max-petal 5x power bonus harvest                       |
| `farm_cactus.py`      | Shearsort + cascade harvest (yield = count^2)          |
| `farm_maze.py`        | Right-hand wall follower for gold                      |
| `farm_dino.py`        | Serpentine tail fill for bones                         |
| `farm_polyculture.py` | Companion planting for yield bonus                     |
| **Quests**            |                                                        |
| `quest_reset.py`      | Full fastest-reset automation (all unlocks from zero)  |
| **Fun**               |                                                        |
| `fun_mandala.py`      | Concentric crop rings (visual art)                     |
| `fun_flipshow.py`     | Drone acrobatics with hat changes                      |
| `fun_conway.py`       | Conway's Game of Life on the farm                      |
| **Reference**         |                                                        |
| `__builtins__.py`     | Game API type stubs for IDE support                    |

## Usage

Every `farm_*` module exposes `once()` (single cycle) and `loop()` (infinite)

### Single farm

```python
import farm_carrot
farm_carrot.loop()
```

### Combine farms

```python
import farm_hay
import farm_wood

while True:
    farm_hay.once()
    farm_wood.once()
```

### Fastest reset

Self-contained, no imports needed:

```python
leaderboard_run(Leaderboards.Fastest_Reset, "quest_reset", 256)
```

### Fun scripts

Fun scripts also expose `once()` / `loop()`

They slow execution for visibility:

```python
import fun_conway
fun_conway.once()
```

## Game Mechanics

| Crop      | Yield formula                 | Growth | Key mechanic                                    |
| --------- | ----------------------------- | ------ | ----------------------------------------------- |
| Grass     | count                         | 0.5s   | Grows on grassland, no water needed             |
| Bush      | count                         | 4s     | Grows on any ground                             |
| Tree      | count                         | 7s     | Slower if adjacent to other trees               |
| Carrot    | count                         | 6s     | Soil + water                                    |
| Pumpkin   | count^3                       | 2s     | All must be alive; 1-in-5 dies                  |
| Sunflower | count (5x if max-petal first) | 5s     | Harvest highest-petal first with 10+ sunflowers |
| Cactus    | count^2                       | 1s     | Must be sorted by size; cascade from smallest   |
| Dinosaur  | fills grid                    | 0.2s   | Wear Dinosaur Hat, tail fills visited tiles     |
| Maze      | world_size gold               | --     | Right-hand wall follower to reach treasure      |

**Companions**: With Polyculture unlocked, `get_companion()` reveals what each plant wants nearby - fulfilling the preference boosts yield

**Fertilizer**: `use_item(Items.Fertilizer)` removes 2s from a plant's remaining grow time

## Unlock Requirements

| Module             | Requires                   |
| ------------------ | -------------------------- |
| Core + basic farms | Import                     |
| `farm_cactus`      | Import                     |
| `farm_maze`        | Import, Dictionaries       |
| `farm_dino`        | Import                     |
| `farm_polyculture` | Import, Lists, Polyculture |
| `fun_mandala`      | Import                     |
| `fun_flipshow`     | Import                     |
| `fun_conway`       | Import, Lists              |
| `quest_reset`      | Nothing (self-contained)   |

## CI

A GitHub Actions workflow runs `ci/lint.py` on push/PR when `*.py`, `ci/**`, or workflow files change

The linter runs three passes:

| Pass        | What it checks                                                                                 |
| ----------- | ---------------------------------------------------------------------------------------------- |
| Syntax      | All `.py` files parse without errors                                                           |
| Conventions | Core: function-only; Farm/Fun: expose `once()` + `loop()`; Quest: no imports; no `import move` |
| README sync | Every script has a Modules table row and vice-versa                                            |

Run locally:

```bash
python ci/lint.py
```

## Algorithms

- **Shearsort** (`farm_cactus`): Alternating row/column bubble-sort passes until sorted. Cacti must be in ascending order for cascade harvest from (0,0) to maximize count^2 yield.
- **Right-hand wall follower** (`farm_maze`): Classic maze-solving algorithm. Always try: turn right, go straight, turn left, reverse. Guarantees reaching treasure in any simply-connected maze.
- **Boustrophedon** (`farm_dino`): Serpentine traversal (East to edge, North, West to edge, North, ...) fills every tile exactly once. Adapts to any world size.
- **Conway's Game of Life** (`fun_conway`): Reads grid state into a list, computes neighbors in-memory (toroidal wrap), then applies births/deaths. Avoids read-during-write corruption.

> **Read-only mirror**: this repository is automatically synced from a private Gitea instance
