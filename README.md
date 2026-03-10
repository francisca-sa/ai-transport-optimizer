### 2030 World Cup: AI Transport Route Optimizer ⚽🌍

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![OpenWeather](https://img.shields.io/badge/API-OpenWeather-orange.svg)](https://openweathermap.org/)

#### 📌 About the Project
This project was developed for the "Fundamentos de Inteligência Artificial" (Fundamentals of Artificial Intelligence) course as part of the Data Science Bachelor's program at the University of Minho. 

The goal is to optimize the distribution of public transportation (buses, trains, metro, airplanes, and taxis) for the massive influx of visitors expected during the 2030 FIFA World Cup, hosted by Portugal, Spain, and Morocco. The system guarantees efficient coverage of priority zones (15 selected stadiums) while strictly adhering to real-world constraints.

⚠️ **Note on Data Simulation:** To create a realistic environment for this project, the dataset, including stadium selections, transport routes, travel times, capacities, and costs, was entirely simulated by our team. While heavily inspired by real-world geography and the anticipated logistics of the 2030 World Cup, this is synthetic data designed specifically to test our AI search algorithms.

#### ⚙️ Core Challenges & System Features
The scenario is modeled as a deterministic search problem on a graph where nodes are stadiums, stations, or airports, and edges are weighted routes. The system dynamically handles several complex constraints:
* **Dynamic Weather Conditions:** Integrates the [OpenWeather API](https://openweathermap.org/) to adjust travel costs and times based on real-time weather (e.g., extreme storms multiply travel times and costs). A local cache with a 1-hour refresh rate is used to optimize API calls, ensuring weather data remains accurate without overloading the system.
* **Vehicle Constraints:** Manages maximum passenger capacities and vehicle autonomy limits. For example, a taxi journey of 600 km requires a refueling stop at 500 km.
* **Time Windows:** Calculates total travel time including waiting times between vehicle departures, managing complex scheduling rules.

#### 🚀 Implemented Search Algorithms
To solve the routing problem, both uninformed and informed search strategies were implemented and compared:

#### Uninformed (Blind) Search
* **Breadth-First Search (BFS):** Guarantees the path with the fewest connections.
* **Depth-First Search (DFS):** Explores a branch to its limit, though it risks finding suboptimal solutions.
* **Uniform Cost Search (UCS):** Expands the node with the lowest accumulated cost, ensuring optimal solutions.
* **K Shortest Simple Paths (Yen):** Iteratively calculates the K shortest paths, guaranteeing diverse solutions without repetitions.

#### Informed (Heuristic) Search
* **Greedy Search:** Focuses exclusively on the heuristic to make extremely fast decisions, though optimality is not guaranteed.
* **A\* (A-Star):** Combines accumulated real cost with a heuristic estimate of the remaining cost to find efficient and optimal paths. Distance calculations for the heuristic use the Haversine formula based on geographical coordinates.

#### 💻 System Architecture & Deployment
The system is highly modular and offers two user interfaces:
* **CLI (Command Line Interface):** An interactive menu for fast testing and debugging.
* **Web Interface (Flask):** A user-friendly web app that processes JSON requests, integrates dynamic weather adjustments, and outputs geographical visualizations using maps.

<img width="846" height="882" alt="image" src="https://github.com/user-attachments/assets/d9228fa1-fd3e-4652-9cc5-68407cbca0e4" />

**Key Modules:**
* `grafo.py`: Constructs the undirected graph from CSV connection data.
* `clima.py`: Handles OpenWeather API calls to dynamically update edge weights based on weather severity.
* `combustivel.py`: Calculates Haversine distances and refueling stops.
* `procuras.py` & `algoritmos.py`: Core routing managers that coordinate and execute the selected search algorithms (BFS, DFS, A*, etc.).
* `tempo.py`: Manages schedules, and total journey durations.
* `config.py`: Centralizes system configurations, including API keys, vehicle autonomy limits, and weather severity dictionaries.
* `main.py` & `app.py`: The primary entry points for the application, handling user inputs for the CLI and Web interfaces, respectively.

#### 🏁 Quick Start (How to Run)
To run this project locally, ensure you have Python installed, then install the required dependencies:

```bash
pip install flask requests
```

To start the Web Interface (Flask):
```bash
python app.py
```
_After running, open `http://127.0.0.1:5000` in your web browser._

To start the Terminal CLI:
```bash
python main.py
```

## 📊 Results & Performance Analysis
To evaluate the algorithms, a case study was conducted for 80 passengers traveling from Estádio D. Afonso Henriques (Guimarães) to Estádio Ibn Batouta (Tanger) with a strict arrival deadline:
* **Uniform Cost & Yen:** Demonstrated the best balance, finding an optimal route costing €115.70 per person with a duration of 24h30m.
* **Greedy Search:** Was the fastest informed algorithm to compute (19h20m travel time) but resulted in an extreme financial cost of €1028.00 per person.
* **A\* (A-Star):** Showed intermediate performance (43h20m travel time and €269.40 cost). This critically indicates that while the algorithm successfully balances time and money, its geographical heuristic function would benefit from further fine-tuning to match the efficiency of Uniform Cost.
* **DFS:** Produced a highly inefficient route taking 80h30m and costing €2882.40, illustrating the risks of depth-first approaches in complex logistical graphs.
  
#### 📁 Repository Structure
```text
ai-transport-optimizer/
│
├── static/
│   └── style.css
|               
├── templates/
│   └── index.html
|
├── algoritmos.py
├── app.py
├── clima.py
├── combustivel.py
├── config.py
├── grafo.py
├── main.py
├── procuras.py
├── tempo.py
├── ligacoes.csv
|
├── docs/
│   └── relatorio.pdf
|
└── README.md
```
#### Authors 
* Adriana Couto
* Francisca Machado | [GitHub](https://github.com/francisca-sa)
* Gabriela Durães
* Maria Inês Castro

_Project developed for the Data Science Bachelor's program at the University of Minho (2024/2025)._
