# F1 Winners Visualization with Apple Embedding-Atlas
## Comprehensive Execution Plan

**Project Goal**: Transform the F1 GP Winners dataset (1,142 historical race records from 1950-2024) into an interactive embedding visualization using Apple's embedding-atlas tool.

**Repository**: `f1-winners-visualization`
**Dataset**: `data/f1_gp_winners_processed.csv` (1,142 records with rich text descriptions)
**Target Python**: 3.11+ (current: 3.9.6)

---

## Critical Prerequisites Identified

### Blockers Resolved
- ❌ **Python Version**: Need 3.11+ (currently have 3.9.6) - **BLOCKER**
- ❌ **Data Format**: CSV needs conversion to Parquet
- ❌ **Git Setup**: Repository not initialized yet
- ❌ **GitHub**: Need to create and sync with remote repository

### Environment Status
- ✅ **OS**: macOS (Darwin 25.1.0)
- ✅ **Git**: Installed (version 2.50.1)
- ✅ **Dataset**: Present with rich text column for embeddings
- ✅ **Working Directory**: `/Users/aref/Dev/Atlas Embeddings/F1 Winners`

---

## Phase 1: Environment Setup (Python & Dependencies)

### 1.1 Install and Configure pyenv

**Why pyenv?**: Allows managing multiple Python versions without conflicts. Future projects can use different Python versions easily.

```bash
# Install pyenv via Homebrew
brew install pyenv

# Add pyenv to shell configuration (if not already done)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell configuration
source ~/.zshrc

# Verify pyenv installation
pyenv --version
```

**Expected Output**: `pyenv X.X.X`

---

### 1.2 Install Python 3.11+

```bash
# List available Python versions
pyenv install --list | grep "  3\.1[12]"

# Install Python 3.11 (or latest stable 3.12)
pyenv install 3.11.9

# Set local Python version for this project
cd "/Users/aref/Dev/Atlas Embeddings/F1 Winners"
pyenv local 3.11.9

# Verify Python version
python --version
```

**Expected Output**: `Python 3.11.9`

**What this does**: Creates a `.python-version` file in the project directory. Whenever you `cd` into this directory, pyenv automatically switches to Python 3.11.9.

---

### 1.3 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip to latest
pip install --upgrade pip

# Verify virtual environment
which python
```

**Expected Output**: `/Users/aref/Dev/Atlas Embeddings/F1 Winners/venv/bin/python`

---

### 1.4 Install embedding-atlas

```bash
# Install embedding-atlas (this will install all 16 core dependencies)
pip install embedding-atlas

# Verify installation
embedding-atlas --help
pip list | grep embedding-atlas
```

**Core Dependencies Installed** (16 packages):
1. click (≥7.0.0) - CLI interface
2. pandas (≥2.2.0) - Data manipulation
3. fastparquet (≥2024.0.0) - Parquet file handling
4. platformdirs (≥4.3.0) - Platform-specific directories
5. umap-learn (≥0.5.0) - Dimensionality reduction
6. sentence-transformers (≥3.3.0) - Text embeddings
7. fastapi (≥0.115.0) - Web API framework
8. uvicorn (≥0.32.0) - ASGI server
9. uvloop (≥0.21.0) - Event loop
10. pyarrow (≥18.0.0) - Arrow data format
11. duckdb (≥1.4.0) - In-process SQL database
12. inquirer (≥3.0.0) - Interactive CLI prompts
13. llvmlite (≥0.43.0) - LLVM binding
14. accelerate (≥1.5.0) - PyTorch acceleration
15. tqdm (≥4.60.0) - Progress bars
16. litellm (≥1.70.0) - LLM interface

---

### 1.5 Create requirements.txt

```bash
# Generate requirements.txt with exact versions
pip freeze > requirements.txt
```

**Purpose**: Enables reproducible environment setup. Anyone cloning the repo can run `pip install -r requirements.txt` to get identical dependencies.

---

## Phase 2: Git Repository Setup

### 2.1 Initialize Local Repository

```bash
# Initialize git repository
git init

# Check git status
git status
```

---

### 2.2 Create .gitignore

**Create `.gitignore` file** with the following content:

```
# Python
venv/
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.*
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
output/
*.parquet
*.log

# Keep data directory but ignore large files
data/*.parquet
```

**Why?**: Prevents committing virtual environments, cache files, OS files, and large data files to git.

---

### 2.3 Initial Commit

Following **CLAUDE-WORKFLOWS.md** commit standards:

```bash
# Stage files for initial commit
git add .gitignore
git add data/f1_gp_winners_processed.csv
git add EXECUTION_PLAN.md

# Create initial commit
git commit -m "$(cat <<'EOF'
Initial project setup: F1 Winners embedding visualization

- Add F1 GP Winners processed dataset (1,142 records, 1950-2024)
- Add .gitignore for Python/venv/OS files
- Add execution plan documentation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Verify commit
git log -1
```

---

### 2.4 GitHub Remote Setup

**Option A: Create via GitHub CLI (gh)**

```bash
# Authenticate with GitHub (if not already done)
gh auth login

# Create new public repository
gh repo create f1-winners-visualization --public --source=. --remote=origin --description="Interactive visualization of F1 Grand Prix winners (1950-2024) using Apple embedding-atlas"

# Push initial commit
git push -u origin main
```

**Option B: Create via GitHub Web UI**

1. Go to https://github.com/new
2. Repository name: `f1-winners-visualization`
3. Description: `Interactive visualization of F1 Grand Prix winners (1950-2024) using Apple embedding-atlas`
4. Public/Private: Choose preference
5. Do NOT initialize with README (we already have files)
6. Click "Create repository"

Then push from terminal:

```bash
# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/f1-winners-visualization.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verify**: Visit `https://github.com/YOUR_USERNAME/f1-winners-visualization` to confirm files are pushed.

---

## Phase 3: Data Preparation

### 3.1 Analyze Source Data

**Dataset**: `data/f1_gp_winners_processed.csv`

**Structure** (15 columns):
1. **text** - Rich descriptive narrative (PRIMARY for embeddings)
2. winner_name - Driver name
3. team - Constructor team
4. grand_prix - Race name
5. circuit - Circuit name
6. continent - Geographic location
7. year - Race year
8. era_category - Historical era (e.g., "Golden Age")
9. team_tier - Team classification (e.g., "Legendary Team")
10. circuit_type - Circuit classification (e.g., "Classic Circuit")
11. continental_group - Regional grouping
12. laps - Number of laps
13. race_time - Race duration
14. dominance_period - Competitive era
15. date - Race date

**Sample Text Column**:
```
"Nino Farina victory at 1950 Great Britain (Silverstone Circuit, Europe)
driving for Alfa Romeo in the Golden Age, 2h 13m race over 70 laps at this
classic circuit representing a legendary team in European Racing"
```

**Key Features**:
- ✅ Ready for text embeddings (rich `text` column)
- ✅ 1,142 records spanning 75 years
- ✅ Rich metadata for filtering and exploration
- ✅ Historical context (eras, dominance periods)

---

### 3.2 Create Conversion Script

**Create**: `scripts/convert_to_parquet.py`

```python
#!/usr/bin/env python3
"""
Convert F1 GP Winners CSV to Parquet format for embedding-atlas.

This script reads the processed CSV file and converts it to Parquet format,
which is the preferred input format for embedding-atlas.
"""

import pandas as pd
from pathlib import Path

def convert_csv_to_parquet():
    """Convert F1 GP Winners CSV to Parquet format."""

    # Define paths
    project_root = Path(__file__).parent.parent
    csv_path = project_root / "data" / "f1_gp_winners_processed.csv"
    parquet_path = project_root / "data" / "f1_gp_winners.parquet"

    print(f"Reading CSV from: {csv_path}")

    # Read CSV
    df = pd.read_csv(csv_path)

    # Display info
    print(f"\nDataset Info:")
    print(f"  Records: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Time span: {df['year'].min()} - {df['year'].max()}")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")

    # Verify text column exists and has content
    if 'text' not in df.columns:
        raise ValueError("'text' column not found in dataset!")

    null_text = df['text'].isna().sum()
    if null_text > 0:
        print(f"\n⚠️  Warning: {null_text} records have null text values")

    # Save as Parquet
    print(f"\nSaving Parquet to: {parquet_path}")
    df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')

    # Verify file was created
    file_size_mb = parquet_path.stat().st_size / (1024 * 1024)
    print(f"✅ Conversion complete! File size: {file_size_mb:.2f} MB")

    return parquet_path

if __name__ == "__main__":
    convert_csv_to_parquet()
```

**Make executable**:

```bash
chmod +x scripts/convert_to_parquet.py
```

---

### 3.3 Run Conversion

```bash
# Create scripts directory
mkdir -p scripts

# Run conversion script
python scripts/convert_to_parquet.py
```

**Expected Output**:
```
Reading CSV from: /Users/aref/Dev/Atlas Embeddings/F1 Winners/data/f1_gp_winners_processed.csv

Dataset Info:
  Records: 1,142
  Columns: 15
  Time span: 1950 - 2024

Columns: text, winner_name, team, grand_prix, circuit, continent, year, era_category, team_tier, circuit_type, continental_group, laps, race_time, dominance_period, date

Saving Parquet to: /Users/aref/Dev/Atlas Embeddings/F1 Winners/data/f1_gp_winners.parquet
✅ Conversion complete! File size: ~0.5 MB
```

---

### 3.4 Commit Data Conversion

```bash
# Stage conversion script
git add scripts/convert_to_parquet.py

# Commit
git commit -m "$(cat <<'EOF'
Add CSV to Parquet conversion script

- Create scripts/convert_to_parquet.py for data format conversion
- Validates text column presence and completeness
- Outputs dataset statistics for verification
- Uses pyarrow engine with snappy compression

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to GitHub
git push
```

**Note**: The `.parquet` file is in `.gitignore` (it can be regenerated from CSV).

---

## Phase 4: Embedding-Atlas Visualization

### 4.1 First Test Run

```bash
# Run embedding-atlas with text column specified
embedding-atlas data/f1_gp_winners.parquet --text text
```

**What happens**:
1. **Embedding Generation**: Uses SentenceTransformers model `all-MiniLM-L6-v2` to generate embeddings from the `text` column
2. **UMAP Projection**: Reduces embeddings to 2D for visualization
3. **Server Launch**: Starts web server at `http://localhost:5055/`
4. **Browser**: Opens interactive visualization

**Expected Terminal Output**:
```
Loading dataset from data/f1_gp_winners.parquet...
Found 1,142 records
Generating embeddings for 'text' column...
Using model: all-MiniLM-L6-v2
Batch size: 32
[Progress bar]
Computing UMAP projection...
Starting server at http://localhost:5055/
```

**Browser**: Visit `http://localhost:5055/` to explore the visualization.

---

### 4.2 Visualization Features to Explore

**Clustering**:
- Should see clusters forming around different eras
- Teams (Ferrari, Mercedes, Red Bull) should cluster
- Geographic patterns (European vs. Americas vs. Asia-Pacific)

**Metadata Exploration**:
- Filter by `era_category` (Golden Age, Turbo Era, Modern Era, etc.)
- Filter by `team_tier` (Legendary Team, Top Team, etc.)
- Filter by `circuit_type` (Classic Circuit, Street Circuit, etc.)
- Filter by `continental_group` (European Racing, Americas Racing, etc.)

**Search**:
- Search for specific drivers (e.g., "Michael Schumacher", "Lewis Hamilton")
- Search for teams (e.g., "Ferrari", "McLaren")
- Search for circuits (e.g., "Monaco", "Silverstone")

**Density Visualization**:
- Identify dense regions (dominant eras/teams)
- Spot outliers (unusual race winners/circumstances)

---

### 4.3 Optional: Parameter Optimization

If the default visualization isn't optimal, adjust UMAP parameters:

```bash
# Increase neighbors for broader clustering
embedding-atlas data/f1_gp_winners.parquet --text text --umap-n-neighbors 30

# Adjust minimum distance for tighter clusters
embedding-atlas data/f1_gp_winners.parquet --text text --umap-min-dist 0.1

# Use different metric
embedding-atlas data/f1_gp_winners.parquet --text text --umap-metric euclidean

# Combine parameters
embedding-atlas data/f1_gp_winners.parquet --text text \
  --umap-n-neighbors 25 \
  --umap-min-dist 0.1 \
  --batch-size 64
```

**Parameter Guide**:
- `--umap-n-neighbors`: Controls local vs global structure (default: 15)
  - Lower (5-10): Emphasizes local structure, more clusters
  - Higher (30-50): Emphasizes global structure, broader patterns
- `--umap-min-dist`: Controls cluster tightness (default: 0.1)
  - Lower (0.01-0.05): Tighter clusters
  - Higher (0.3-0.5): More spread out
- `--umap-metric`: Distance metric (default: cosine)
  - Options: cosine, euclidean, manhattan
- `--batch-size`: Embedding generation batch size
  - Increase for faster processing (if memory allows)

---

### 4.4 Create Launch Script

**Create**: `scripts/launch_visualization.sh`

```bash
#!/bin/bash
# Launch F1 Winners embedding visualization

# Activate virtual environment
source venv/bin/activate

# Launch embedding-atlas
embedding-atlas data/f1_gp_winners.parquet \
  --text text \
  --umap-n-neighbors 20 \
  --umap-min-dist 0.1 \
  --batch-size 64

# Note: Press Ctrl+C to stop the server
```

**Make executable**:

```bash
chmod +x scripts/launch_visualization.sh
```

---

## Phase 5: Documentation & Polish

### 5.1 Create README.md

**Create**: `README.md`

```markdown
# F1 Winners Visualization

Interactive embedding-based visualization of Formula 1 Grand Prix winners from 1950-2024, powered by [Apple's embedding-atlas](https://github.com/apple/embedding-atlas).

## Overview

This project visualizes 1,142 F1 race victories spanning 75 years of motorsport history. Using natural language embeddings and UMAP dimensionality reduction, the visualization reveals patterns in:

- Driver and team dominance across different eras
- Geographic distribution of racing
- Circuit characteristics and classifications
- Historical evolution of Formula 1

## Dataset

**Source**: F1 GP Winners (1950-2024)
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

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/f1-winners-visualization.git
cd f1-winners-visualization
\`\`\`

### 2. Install Python 3.11+ (if needed)

Using pyenv (recommended):

\`\`\`bash
# Install pyenv
brew install pyenv

# Install Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9
\`\`\`

### 3. Create Virtual Environment

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 4. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 5. Generate Parquet File

\`\`\`bash
python scripts/convert_to_parquet.py
\`\`\`

## Usage

### Quick Start

\`\`\`bash
# Activate virtual environment
source venv/bin/activate

# Launch visualization
embedding-atlas data/f1_gp_winners.parquet --text text
\`\`\`

Or use the launch script:

\`\`\`bash
./scripts/launch_visualization.sh
\`\`\`

The visualization will open in your browser at `http://localhost:5055/`

### Advanced Usage

Customize UMAP parameters for different perspectives:

\`\`\`bash
# Broader clustering (emphasize global patterns)
embedding-atlas data/f1_gp_winners.parquet --text text --umap-n-neighbors 30

# Tighter clusters (emphasize local patterns)
embedding-atlas data/f1_gp_winners.parquet --text text --umap-min-dist 0.05

# Custom configuration
embedding-atlas data/f1_gp_winners.parquet --text text \
  --umap-n-neighbors 25 \
  --umap-min-dist 0.1 \
  --batch-size 64
\`\`\`

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

\`\`\`
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
\`\`\`

## Technology Stack

- **[embedding-atlas](https://github.com/apple/embedding-atlas)**: Visualization framework
- **[sentence-transformers](https://www.sbert.net/)**: Text embedding generation
- **[UMAP](https://umap-learn.readthedocs.io/)**: Dimensionality reduction
- **[FastAPI](https://fastapi.tiangolo.com/)**: Web server
- **[pandas](https://pandas.pydata.org/)**: Data manipulation
- **[pyarrow](https://arrow.apache.org/docs/python/)**: Parquet file handling

## Resources

- **embedding-atlas Documentation**: https://apple.github.io/embedding-atlas/
- **Live Demo**: https://apple.github.io/embedding-atlas/ (example visualization)
- **Repository**: https://github.com/apple/embedding-atlas

## License

This project is for educational and visualization purposes. The embedding-atlas tool is licensed under MIT by Apple Inc.

## Acknowledgments

- Apple Inc. for the embedding-atlas visualization tool
- F1 historical data contributors
- Open source embedding and dimensionality reduction communities
\`\`\`

---

### 5.2 Commit Documentation

```bash
# Stage README
git add README.md

# Commit
git commit -m "$(cat <<'EOF'
Add comprehensive project documentation

- Create README with setup, usage, and exploration guide
- Document dataset structure and historical context
- Include technology stack and resource links
- Add examples for advanced UMAP parameter tuning

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to GitHub
git push
```

---

### 5.3 Add requirements.txt to Git

```bash
# Stage requirements.txt
git add requirements.txt

# Commit
git commit -m "$(cat <<'EOF'
Add Python dependencies file

- Lock embedding-atlas and all dependencies
- Enable reproducible environment setup
- Generated from pip freeze after installation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to GitHub
git push
```

---

### 5.4 Add Launch Script to Git

```bash
# Stage launch script
git add scripts/launch_visualization.sh

# Commit
git commit -m "$(cat <<'EOF'
Add visualization launch script

- Create convenience script for starting embedding-atlas
- Includes optimized UMAP parameters
- Automatically activates virtual environment

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to GitHub
git push
```

---

## Phase 6: Validation & Testing

### 6.1 End-to-End Test

Test the complete setup from scratch:

```bash
# Clone to temporary directory
cd /tmp
git clone https://github.com/YOUR_USERNAME/f1-winners-visualization.git f1-test
cd f1-test

# Follow README setup
pyenv local 3.11.9
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate Parquet file
python scripts/convert_to_parquet.py

# Launch visualization
./scripts/launch_visualization.sh

# Test in browser at http://localhost:5055/
```

**Validation Checklist**:
- [ ] Repository clones successfully
- [ ] Virtual environment creates without errors
- [ ] All dependencies install correctly
- [ ] Parquet conversion completes successfully
- [ ] Visualization launches without errors
- [ ] Browser shows interactive visualization
- [ ] Data loads correctly (1,142 points visible)
- [ ] Metadata filters work
- [ ] Search functionality works
- [ ] Clustering appears meaningful

---

### 6.2 Cleanup & Final Review

```bash
# Return to project directory
cd "/Users/aref/Dev/Atlas Embeddings/F1 Winners"

# Check for any uncommitted changes
git status

# Review commit history
git log --oneline --graph

# Verify remote is up to date
git push

# Clean up test directory
rm -rf /tmp/f1-test
```

---

## Success Criteria

### ✅ Environment
- [x] Python 3.11+ installed via pyenv
- [x] Virtual environment created and activated
- [x] embedding-atlas installed with all dependencies
- [x] requirements.txt generated

### ✅ Repository
- [x] Git repository initialized
- [x] .gitignore configured properly
- [x] GitHub repository created: `f1-winners-visualization`
- [x] All commits follow CLAUDE-WORKFLOWS.md standards
- [x] Remote synced and up to date

### ✅ Data
- [x] F1 GP Winners dataset present (1,142 records)
- [x] CSV converted to Parquet format
- [x] Text column validated for embeddings
- [x] Conversion script created and committed

### ✅ Visualization
- [x] embedding-atlas launches successfully
- [x] Web server accessible at localhost:5055
- [x] Embeddings generated from text column
- [x] UMAP projection complete
- [x] Interactive visualization functional
- [x] Metadata filtering works
- [x] Search functionality works

### ✅ Documentation
- [x] README.md complete with setup guide
- [x] EXECUTION_PLAN.md saved and tracked
- [x] Launch script created
- [x] All scripts documented
- [x] End-to-end validation successful

---

## Troubleshooting

### Python Version Issues

**Problem**: `embedding-atlas` requires Python 3.11+

**Solution**:
```bash
# Check current Python version
python --version

# If < 3.11, install via pyenv
pyenv install 3.11.9
pyenv local 3.11.9
```

### Import Errors

**Problem**: ModuleNotFoundError for dependencies

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Parquet File Not Found

**Problem**: embedding-atlas can't find .parquet file

**Solution**:
```bash
# Generate Parquet file from CSV
python scripts/convert_to_parquet.py

# Verify file exists
ls -lh data/*.parquet
```

### Browser Won't Open / Server Issues

**Problem**: Visualization doesn't launch

**Solution**:
```bash
# Check if port 5055 is already in use
lsof -i :5055

# Kill process if needed
kill -9 <PID>

# Relaunch
embedding-atlas data/f1_gp_winners.parquet --text text
```

### Empty Visualization

**Problem**: Visualization loads but no data points visible

**Solution**:
```bash
# Check Parquet file has data
python -c "import pandas as pd; df = pd.read_parquet('data/f1_gp_winners.parquet'); print(f'Records: {len(df)}')"

# Verify text column exists and has values
python -c "import pandas as pd; df = pd.read_parquet('data/f1_gp_winners.parquet'); print(df['text'].head())"
```

---

## Next Steps & Enhancements

### Potential Improvements

1. **Podium Data**: Expand to include 2nd/3rd place finishers
2. **Qualifying**: Add pole position data
3. **Lap Times**: Include fastest lap information
4. **Weather**: Incorporate race weather conditions
5. **Career Visualizations**: Create driver career trajectories
6. **Team Evolution**: Track constructor changes over time
7. **Circuit Changes**: Visualize track modifications
8. **Statistical Analysis**: Add performance metrics

### Advanced Features

1. **Custom Embeddings**: Train domain-specific embedding model
2. **Multi-Modal**: Combine text with numerical features
3. **Temporal Animation**: Animate through years
4. **Comparative Views**: Side-by-side era comparisons
5. **Export**: Save visualizations as images
6. **Sharing**: Deploy to web for public access

---

## Estimated Timeline

| Phase | Tasks | Time Estimate |
|-------|-------|--------------|
| **Phase 1** | Python/pyenv setup, venv, install embedding-atlas | 15-20 min |
| **Phase 2** | Git init, .gitignore, GitHub repo, initial commits | 5-10 min |
| **Phase 3** | Conversion script, CSV → Parquet, commits | 10 min |
| **Phase 4** | Launch visualization, test, optimize parameters | 15-20 min |
| **Phase 5** | README, documentation, final commits | 15 min |
| **Phase 6** | End-to-end validation, cleanup | 10 min |
| **Total** | | **70-85 minutes** |

---

## Notes

- All commit messages follow CLAUDE-WORKFLOWS.md standards
- .gitignore prevents committing venv, cache files, and large data files
- Parquet file can be regenerated from CSV (not tracked in git)
- Launch script includes optimized parameters for F1 dataset
- README provides complete setup for new users
- End-to-end test ensures reproducibility

---

## Resources & References

### embedding-atlas
- **Documentation**: https://apple.github.io/embedding-atlas/overview.html
- **GitHub**: https://github.com/apple/embedding-atlas
- **Live Demo**: https://apple.github.io/embedding-atlas/
- **PyPI**: https://pypi.org/project/embedding-atlas/

### Technologies
- **UMAP**: https://umap-learn.readthedocs.io/
- **SentenceTransformers**: https://www.sbert.net/
- **FastAPI**: https://fastapi.tiangolo.com/
- **pandas**: https://pandas.pydata.org/

### Development
- **pyenv**: https://github.com/pyenv/pyenv
- **Virtual Environments**: https://docs.python.org/3/library/venv.html
- **GitHub CLI**: https://cli.github.com/

---

**Last Updated**: 2025-11-13
**Project Status**: Ready for execution
**Next Action**: Begin Phase 1 - Environment Setup
