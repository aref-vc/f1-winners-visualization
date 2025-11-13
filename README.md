# F1 Winners Visualization

Interactive embedding-based visualization of Formula 1 Grand Prix winners from 1950-2025, powered by [Apple's embedding-atlas](https://github.com/apple/embedding-atlas).

![GitHub](https://img.shields.io/github/license/aref-vc/f1-winners-visualization)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

## Overview

This project visualizes 1,142 F1 race victories spanning 75 years of motorsport history. Using natural language embeddings and UMAP dimensionality reduction, the visualization reveals patterns in:

- **Driver and team dominance** across different eras
- **Geographic distribution** of racing (Europe, Americas, Asia, Middle East)
- **Circuit characteristics** and classifications
- **Historical evolution** of Formula 1 racing

## Dataset

**Source**: F1 GP Winners (1950-2025)
**Records**: 1,142 race victories
**Time Span**: 75 years of F1 history

### Data Structure

Each record includes:
- **Rich text narrative** combining race details, driver, team, circuit, and historical context
- **Driver information**: Name and team
- **Race details**: Grand Prix name, circuit, location, date
- **Historical context**: Era category, dominance period, team tier
- **Technical data**: Laps, race time
- **Geographic data**: Continent, continental grouping
- **Circuit classification**: Type (classic, street, modern, etc.)

### Sample Entry

> "Lewis Hamilton victory at 2024 Bahrain (Bahrain International Circuit, Asia) driving for Mercedes in the Modern Era, 1h 28m race over 57 laps at this modern circuit representing a top team in Middle Eastern Racing"

## Prerequisites

- **Python**: 3.11+ required
- **OS**: macOS, Linux, or Windows
- **Browser**: Modern browser with WebGL 2 or WebGPU support

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/aref-vc/f1-winners-visualization.git
cd f1-winners-visualization
```

### 2. Install Python 3.11+ (if needed)

Using pyenv (recommended):

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9
```

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate Parquet File

```bash
python scripts/convert_to_parquet.py
```

## Usage

### Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Launch visualization
embedding-atlas data/f1_gp_winners.parquet --text text
```

Or use the launch script:

```bash
./scripts/launch_visualization.sh
```

The visualization will open in your browser at `http://localhost:5055/`

### Advanced Usage

Customize UMAP parameters for different perspectives:

```bash
# Broader clustering (emphasize global patterns)
embedding-atlas data/f1_gp_winners.parquet --text text --umap-n-neighbors 30

# Tighter clusters (emphasize local patterns)
embedding-atlas data/f1_gp_winners.parquet --text text --umap-min-dist 0.05

# Custom configuration
embedding-atlas data/f1_gp_winners.parquet --text text \
  --umap-n-neighbors 25 \
  --umap-min-dist 0.1 \
  --batch-size 64
```

## Exploration Guide

### What to Look For

**Era Clustering**:
- Golden Age (1950s): Fangio, Ascari era
- Turbo Era (1980s): Prost, Senna
- Modern Era (2000s+): Schumacher, Hamilton, Verstappen

**Team Dominance**:
- Ferrari dynasties (1950s, 2000s)
- McLaren golden years (1980s-90s)
- Mercedes hybrid era (2014-2020)
- Red Bull dominance (2010-2013, 2021-2024)

**Geographic Patterns**:
- European racing heartland
- Expansion to Americas, Asia, Middle East
- Classic circuits vs modern facilities

**Circuit Types**:
- Street circuits (Monaco, Singapore)
- Classic tracks (Silverstone, Monza, Spa)
- Modern facilities (Bahrain, Abu Dhabi)

### Visualization Features

- **Search**: Find specific drivers, teams, or circuits
- **Filter**: Use metadata to isolate eras, teams, or locations
- **Density View**: Identify dominant periods and outliers
- **Nearest Neighbors**: Discover similar races and patterns

## Project Structure

```
f1-winners-visualization/
├── README.md
├── EXECUTION_PLAN.md
├── requirements.txt
├── .gitignore
├── .python-version
├── data/
│   ├── f1_gp_winners_processed.csv    # Source data
│   └── f1_gp_winners.parquet          # Generated (not in git)
├── scripts/
│   ├── convert_to_parquet.py          # CSV → Parquet conversion
│   └── launch_visualization.sh        # Quick launch script
└── venv/                              # Virtual environment (not in git)
```

## Technology Stack

- **[embedding-atlas](https://github.com/apple/embedding-atlas)**: Visualization framework
- **[sentence-transformers](https://www.sbert.net/)**: Text embedding generation (all-MiniLM-L6-v2)
- **[UMAP](https://umap-learn.readthedocs.io/)**: Dimensionality reduction
- **[FastAPI](https://fastapi.tiangolo.com/)**: Web server
- **[pandas](https://pandas.pydata.org/)**: Data manipulation
- **[pyarrow](https://arrow.apache.org/docs/python/)**: Parquet file handling

## Resources

- **embedding-atlas Documentation**: https://apple.github.io/embedding-atlas/
- **Live Demo**: https://apple.github.io/embedding-atlas/ (example visualization)
- **GitHub Repository**: https://github.com/aref-vc/f1-winners-visualization

## License

This project is for educational and visualization purposes. The embedding-atlas tool is licensed under MIT by Apple Inc.

## Acknowledgments

- Apple Inc. for the embedding-atlas visualization tool
- F1 historical data contributors
- Open source embedding and dimensionality reduction communities
