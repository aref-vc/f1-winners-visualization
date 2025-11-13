# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

F1 Winners Visualization is an interactive embedding-based visualization of 1,142 Formula 1 Grand Prix victories from 1950-2025. The project uses Apple's embedding-atlas framework to create a 2D visualization of race data, revealing patterns in driver dominance, team performance, geographic distribution, and historical evolution of F1 racing.

**Key Technology**: Apple embedding-atlas (visualization framework) + sentence-transformers (text embeddings) + UMAP (dimensionality reduction)

**Data Flow**: CSV → Parquet → Text Embeddings (384-dim) → UMAP Projection (2D) → Interactive Web Visualization

## Environment Requirements

- **Python**: 3.11+ (CRITICAL - embedding-atlas requires 3.11+, project uses 3.11.9 via pyenv)
- **Port**: 5055 (embedding-atlas default, documented in global CLAUDE-PORTS.md)
- **Browser**: WebGL 2 or WebGPU support required for visualization

## Essential Commands

### Environment Setup
```bash
# Activate pyenv environment
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version  # Must show 3.11.9
```

### Data Processing
```bash
# Convert CSV to Parquet (required before visualization)
python scripts/convert_to_parquet.py

# Output: data/f1_gp_winners.parquet (excluded from git)
```

### Launch Visualization
```bash
# Quick launch (recommended)
./scripts/launch_visualization.sh

# Manual launch
embedding-atlas data/f1_gp_winners.parquet --text text

# Custom UMAP parameters
embedding-atlas data/f1_gp_winners.parquet --text text \
  --umap-n-neighbors 20 \
  --umap-min-dist 0.1 \
  --batch-size 64

# Server runs at: http://localhost:5055/
```

### Dependency Management
```bash
# Install all dependencies
pip install -r requirements.txt

# Core dependency: embedding-atlas (pulls 50+ packages)

# Update requirements
pip freeze > requirements.txt
```

## Architecture

### Data Pipeline

1. **Source Data** (`data/f1_gp_winners_processed.csv`)
   - 1,142 records spanning 1950-2025
   - 15 columns with rich metadata
   - **Critical column**: `text` - Rich narrative descriptions used for embeddings
   - Example: "Lewis Hamilton victory at 2024 Bahrain (Bahrain International Circuit, Asia) driving for Mercedes..."

2. **Conversion** (`scripts/convert_to_parquet.py`)
   - Reads CSV using pandas
   - Validates `text` column presence
   - Exports to Parquet with pyarrow + snappy compression
   - Output: ~0.07 MB optimized file

3. **Embedding Generation** (embedding-atlas automatic)
   - Model: `all-MiniLM-L6-v2` (SentenceTransformers)
   - Converts text → 384-dimensional vectors
   - Batch size: 64 (configurable via `--batch-size`)
   - Uses Apple Silicon GPU (MPS) when available

4. **Dimensionality Reduction** (UMAP)
   - 384-dim vectors → 2D coordinates
   - Default parameters:
     - `n_neighbors=20` (balance local/global structure)
     - `min_dist=0.1` (moderate cluster tightness)
     - `metric=cosine` (standard for text embeddings)

5. **Visualization Server** (FastAPI + uvicorn)
   - Serves interactive web application
   - Real-time search, filtering, density views
   - WebGPU rendering with WebGL 2 fallback

### Key Files

- `data/f1_gp_winners_processed.csv` - Source dataset (committed)
- `data/f1_gp_winners.parquet` - Converted data (generated, excluded from git)
- `scripts/convert_to_parquet.py` - Data conversion utility
- `scripts/launch_visualization.sh` - Convenience launcher with pyenv setup
- `requirements.txt` - Python dependencies (generated from pip freeze)
- `.python-version` - Pyenv local version file (3.11.9)

### Dataset Schema

**15 Columns** (CSV structure):
- `text` - Primary field for embeddings (rich narrative combining all metadata)
- `winner_name`, `team` - Driver and constructor
- `grand_prix`, `circuit`, `continent` - Race location details
- `year`, `date` - Temporal information
- `era_category` - Historical era (Golden Age, Turbo Era, Modern Era, etc.)
- `team_tier` - Team classification (Legendary Team, Top Team, etc.)
- `circuit_type` - Circuit classification (Classic, Street, Modern, Historic Venue)
- `continental_group` - Regional grouping (European Racing, Americas Racing, etc.)
- `laps`, `race_time` - Technical race data
- `dominance_period` - Competitive era (Independent Era, Ferrari Dominance, etc.)

**Metadata Usage**: All columns except `text` are available as filters and search fields in the visualization.

## UMAP Parameter Tuning

The visualization can be customized by adjusting UMAP parameters:

**For broader clustering** (emphasize global patterns):
```bash
--umap-n-neighbors 30  # Higher = more global structure
```

**For tighter clusters** (emphasize local patterns):
```bash
--umap-min-dist 0.05  # Lower = tighter grouping
```

**Trade-offs**:
- `n_neighbors`: 5-10 (local) vs 30-50 (global). Default: 15, Project uses: 20
- `min_dist`: 0.01-0.05 (tight) vs 0.3-0.5 (spread). Default: 0.1
- `metric`: cosine (recommended for text), euclidean, manhattan

## Expected Visualization Patterns

When the visualization loads, expect to see clustering around:

1. **Eras**: Golden Age (1950s), Turbo Era (1980s), Modern Era (2000s+)
2. **Teams**: Ferrari dynasties, Mercedes hybrid era, Red Bull dominance
3. **Geography**: European heartland vs global expansion (Asia, Middle East, Americas)
4. **Circuits**: Street circuits (Monaco, Singapore) vs classic tracks (Silverstone, Monza)

**Validation**: If clusters don't form or points appear random, check:
- Text column has meaningful content
- Embeddings generated successfully (check console output)
- UMAP parameters are appropriate for dataset size

## Git Workflow Notes

This project follows the git commit standards defined in `~/.claude/CLAUDE-WORKFLOWS.md`:

- Commit messages include emoji prefixes and Claude Code co-authorship
- `.parquet` files excluded from git (regenerated from CSV)
- Virtual environment and dependencies excluded via `.gitignore`

## GitHub Repository

**URL**: https://github.com/aref-vc/f1-winners-visualization
**Status**: ✅ Completed & deployed locally

## Troubleshooting

**Port 5055 already in use**:
```bash
lsof -i :5055  # Find process
kill -9 <PID>  # Terminate if needed
```

**Python version mismatch**:
```bash
pyenv local 3.11.9  # Set correct version
python --version     # Verify
```

**Missing Parquet file**:
```bash
python scripts/convert_to_parquet.py  # Regenerate
```

**Empty visualization / no data points**:
- Check Parquet file exists and has data
- Verify `text` column exists and populated
- Check console for embedding generation errors

## Related Documentation

- `EXECUTION_PLAN.md` - Detailed setup guide with step-by-step instructions
- `README.md` - User-facing documentation with exploration guide
- `~/.claude/CLAUDE-PROJECTS.md` - Project tracking and milestones
- `~/.claude/CLAUDE-PORTS.md` - Port allocation (5055 registered)
- embedding-atlas docs: https://apple.github.io/embedding-atlas/
