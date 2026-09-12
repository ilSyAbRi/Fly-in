
# Fly-in

> [!IMPORTANT]
> **Press `Alt + f4` to exit the graphical interface.** <br>
> **do : `make` or `make help` for info.**<br>
> **all info inside `make` or `make help` are correct by 95%.**

#### 📄 Project Subject
[Read the project subject](en.subject.pdf)

## Description

**Fly-in** is a turn-based drone pathfinding simulation written in Python.

The program reads a map describing drones, zones, zone types, capacities, and connections. It builds a graph from that map, computes valid routes from the start hub to the end hub, and simulates drone movement turn by turn while respecting zone and connection capacities.

The project also includes an Arcade-based visualizer to display the graph and drone movements.

## Instructions

### Requirements

- Python 3.10+
- Make

### Install dependencies

```bash
make install
```

### Run the project

Using the Makefile:

```bash
make run MAP=maps/easy/01_linear_path.txt
```

Or directly:

```bash
python3 main.py maps/easy/01_linear_path.txt
```

If no map path is provided, the program uses the default map.

### Visualizer controls

- `W` / `Up Arrow` — move camera up
- `S` / `Down Arrow` — move camera down
- `A` / `Left Arrow` — move camera left
- `D` / `Right Arrow` — move camera right
- `Space` — advance the simulation by one turn
- Hold `Space` — continuously advance through turns

## Algorithm explanation

Fly-in uses a graph-based pathfinding system.

Each zone is represented as a node and each connection between two zones is represented as an edge.

Zone traversal costs are:

- **normal** — 1 turn
- **priority** — 1 turn
- **restricted** — 2 turns
- **blocked** — cannot be entered

### Heuristic calculation

Before searching for drone paths, the program calculates the minimum known distance from each reachable zone to the end hub.

This is done using a Dijkstra-style search starting from the end hub.

The calculated distances are used as the heuristic for the main pathfinding search.

The heuristic calculation also allows the program to detect disconnected parts of the graph.

### Pathfinding

The main pathfinding algorithm uses an A*-style priority queue.

For each possible movement, the algorithm considers the current turn, movement cost, and estimated remaining distance to the end.

Conceptually:

```text
f = arrival turn + estimated distance to the end
```

A search state contains both the zone and the turn:

```text
(zone, turn)
```

The turn is part of the state because a zone can be available during one turn but full during another.

The pathfinder also considers:

- zone capacity (`max_drones`)
- connection capacity (`max_link_capacity`)
- waiting in the current zone
- restricted zones that require two turns to enter
- priority zones as a tie-breaker

Drones are planned sequentially.

After the path of one drone is calculated, the zones and connections used by that drone are recorded. The next drone is then planned while respecting those reservations.

This prevents drones from exceeding zone or connection capacity during the same turn.

## Visual representation

Fly-in includes a graphical visualization built using Arcade.

The visualizer displays:

- zones as circles
- zone names above their circles
- connections as lines between zones
- drones as smaller circles
- the current simulation turn
- camera movement for navigating larger maps

Zone types are represented using labels:

```text
N = Normal
R = Restricted
P = Priority
```

The visualization makes it easier to understand how drones move through the graph over time.

It also helps show:

- drones waiting for available capacity
- movement through restricted zones
- different paths through the graph
- multiple drones moving at the same time
- the structure of larger maps

The camera can be moved with the keyboard so maps that extend beyond the initial screen can still be explored.

## Example input

```text
nb_drones: 2
start_hub: Start 0 0
hub: A 1 0
end_hub: End 2 0

connection: Start-A
connection: A-End
```

This map contains two drones traveling from `Start` to `End` through zone `A`.

## Expected output

```text
D1-A
D1-End D2-A
D2-End
```

Each output line represents one simulation turn.

A normal drone movement is displayed as:

```text
DRONE-ZONE
```

For movement through a restricted connection, the output can contain both sides of the connection:

```text
DRONE-FROM-TO
```

## Project structure

```text
.
├── main.py
├── parser.py
├── models.py
├── graph.py
├── pathfinding.py
├── engine.py
├── display.py
├── maps/
├── Makefile
└── README.md
```

### Files

- `main.py` — starts the program and connects all components
- `parser.py` — reads and validates map files
- `models.py` — defines zones, connections, and drones
- `graph.py` — builds the graph representation
- `pathfinding.py` — calculates and schedules drone paths
- `engine.py` — executes simulation turns and produces output
- `display.py` — provides the Arcade graphical visualization

## 🎮 Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move camera up |
| `S` / `↓` | Move camera down |
| `A` / `←` | Move camera left |
| `D` / `→` | Move camera right |
| `Space` | Advance the simulation by one turn |
| `Alt + 4` | Exit the graphical interface |

> [!IMPORTANT]
> **Press `Alt + f4` to exit the graphical interface.** <br>
> **do : `make` or `make help` for info.** <br>
> **all info inside `make` or `make help` are correct by 95%.**
