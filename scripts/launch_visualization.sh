#!/bin/bash
# Launch F1 Winners embedding visualization

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

# Setup pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Activate virtual environment
source venv/bin/activate

# Launch embedding-atlas with optimized parameters for F1 dataset
echo "🏎️  Launching F1 Winners Visualization..."
echo "📊 Dataset: 1,142 F1 race victories (1950-2025)"
echo "🌐 Server will start at: http://localhost:5055/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

embedding-atlas data/f1_gp_winners.parquet \
  --text text \
  --umap-n-neighbors 20 \
  --umap-min-dist 0.1 \
  --batch-size 64
