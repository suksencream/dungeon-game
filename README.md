# Dungeon Game - Heuristic Search Algorithm Demonstration

A dungeon exploration game that demonstrates various heuristic search algorithms for pathfinding and AI navigation. This project showcases the implementation and comparison of different search algorithms in a practical gaming context.

## 🎯 Project Overview

This project implements a dungeon game where players navigate through procedurally generated or predefined dungeon layouts. The primary focus is on demonstrating heuristic search algorithms, particularly A* (A-star), for optimal pathfinding and intelligent enemy AI behavior.

### Key Features

- **Interactive dungeon exploration** with player movement mechanics
- **Multiple search algorithm implementations** for pathfinding
- **Intelligent enemy AI** using heuristic search for navigation
- **Visual demonstration** of algorithm performance and path optimization
- **Procedural dungeon generation** (if applicable)
- **Performance comparison** between different search algorithms

## 🧠 Heuristic Search Algorithms Implemented

### A* (A-Star) Search
- **Purpose**: Optimal pathfinding with heuristic guidance
- **Heuristic**: Manhattan distance for grid-based movement
- **Use Cases**: Player pathfinding, enemy navigation, optimal route planning

### Dijkstra's Algorithm
- **Purpose**: Guaranteed shortest path without heuristics
- **Use Cases**: Baseline comparison for A* performance

### Breadth-First Search (BFS)
- **Purpose**: Unweighted shortest path search
- **Use Cases**: Simple pathfinding when all moves have equal cost

### Depth-First Search (DFS)
- **Purpose**: Exploration and maze generation
- **Use Cases**: Dungeon generation, connectivity testing

## 🚀 Getting Started

### Prerequisites

```bash
# Example for different programming languages
# For Python:
Python 3.8+
pygame (for graphics)
numpy (for calculations)

# For Java:
Java 11+
JavaFX (for UI)

# For C++:
C++17 or later
SDL2 (for graphics)
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/suksencream/dungeon-game.git
   cd dungeon-game
   ```

2. **Install dependencies**
   ```bash
   # For Python example:
   pip install -r requirements.txt
   
   # For Java example:
   # Ensure JavaFX is properly configured
   ```

3. **Run the game**
   ```bash
   # Python example:
   python main.py
   
   # Java example:
   java -jar dungeon-game.jar
   ```

## 🎮 How to Play

### Controls
- **Arrow Keys / WASD**: Move player character
- **Space**: Interact with objects
- **M**: Show/hide minimap
- **P**: Pause game
- **R**: Restart level
- **H**: Show heuristic visualization (if available)

### Objective
Navigate through the dungeon, avoid or defeat enemies, collect treasures, and reach the exit. The game demonstrates how different pathfinding algorithms affect gameplay and AI behavior.

## 🔍 Algorithm Demonstration Features

### Visual Pathfinding
- **Real-time visualization** of algorithm execution
- **Path highlighting** showing optimal routes
- **Node exploration visualization** displaying searched areas
- **Performance metrics** (time taken, nodes explored, path length)

### Comparative Analysis
The game allows switching between different algorithms to compare:
- **Execution time** and efficiency
- **Path optimality** and length
- **Memory usage** (nodes explored)
- **Practical performance** in gaming scenarios

### Enemy AI Behavior
Enemies use heuristic search for:
- **Player tracking** and pursuit
- **Obstacle avoidance** during navigation
- **Patrol route optimization**
- **Strategic positioning** in combat scenarios

## 📁 Project Structure

```
dungeon-game/
├── src/
│   ├── algorithms/           # Search algorithm implementations
│   │   ├── astar.py/java/cpp
│   │   ├── dijkstra.py/java/cpp
│   │   ├── bfs.py/java/cpp
│   │   └── dfs.py/java/cpp
│   ├── game/                 # Game mechanics and logic
│   │   ├── player.py/java/cpp
│   │   ├── enemy.py/java/cpp
│   │   ├── dungeon.py/java/cpp
│   │   └── pathfinder.py/java/cpp
│   ├── ui/                   # User interface components
│   │   ├── renderer.py/java/cpp
│   │   ├── input_handler.py/java/cpp
│   │   └── hud.py/java/cpp
│   └── utils/                # Utility functions
│       ├── grid.py/java/cpp
│       └── heuristics.py/java/cpp
├── assets/                   # Game assets (sprites, sounds, etc.)
├── data/                     # Level data and configurations
├── docs/                     # Documentation and algorithm explanations
├── tests/                    # Unit tests for algorithms
├── README.md
└── requirements.txt/pom.xml/CMakeLists.txt
```

## 🧪 Algorithm Implementation Details

### A* Algorithm
```python
def a_star(start, goal, grid):
    """
    A* pathfinding algorithm implementation
    Uses Manhattan distance as heuristic function
    """
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while not open_set.empty():
        current = open_set.get()[1]
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + distance(current, neighbor)
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                open_set.put((f_score[neighbor], neighbor))
    
    return None  # No path found
```

### Heuristic Functions
- **Manhattan Distance**: `|x1 - x2| + |y1 - y2|` (for grid-based movement)
- **Euclidean Distance**: `sqrt((x1-x2)² + (y1-y2)²)` (for diagonal movement)
- **Chebyshev Distance**: `max(|x1-x2|, |y1-y2|)` (for 8-directional movement)

## 📊 Performance Analysis

The game includes built-in benchmarking tools to analyze algorithm performance:

| Algorithm | Time Complexity | Space Complexity | Optimality | Use Case |
|-----------|----------------|------------------|------------|----------|
| A* | O(b^d) | O(b^d) | Optimal* | General pathfinding |
| Dijkstra | O((V+E)logV) | O(V) | Optimal | Shortest path guarantee |
| BFS | O(V+E) | O(V) | Optimal** | Unweighted graphs |
| DFS | O(V+E) | O(V) | Not optimal | Exploration, generation |

*Optimal with admissible heuristic  
**Optimal for unweighted graphs

## 🎯 Educational Objectives

This project demonstrates:

1. **Practical application** of theoretical algorithms in game development
2. **Performance trade-offs** between different search strategies
3. **Heuristic design** and its impact on algorithm efficiency
4. **Real-time pathfinding** in interactive applications
5. **AI behavior** implementation using search algorithms

## 🔧 Configuration

### Algorithm Settings
Modify `config.json` or similar configuration file:
```json
{
  "default_algorithm": "astar",
  "heuristic_function": "manhattan",
  "visualization_enabled": true,
  "step_delay": 50,
  "grid_size": {
    "width": 50,
    "height": 50
  }
}
```

### Performance Tuning
- **Grid resolution**: Affects pathfinding complexity
- **Update frequency**: Balance between responsiveness and performance
- **Visualization detail**: Toggle for better performance
- **Heuristic weighting**: Adjust for speed vs. optimality trade-off

## 🧪 Running Tests

```bash
# Run all algorithm tests
python -m pytest tests/

# Run specific algorithm tests
python -m pytest tests/test_astar.py

# Run performance benchmarks
python tests/benchmark_algorithms.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-algorithm`)
3. Implement your changes with proper documentation
4. Add tests for new algorithms
5. Submit a pull request

### Adding New Algorithms
To add a new search algorithm:
1. Implement the algorithm in `src/algorithms/`
2. Add corresponding tests in `tests/`
3. Update the algorithm selector in the main game loop
4. Document the algorithm's properties and use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*This project serves as both an entertaining game and an educational tool for understanding heuristic search algorithms in practical applications.*
