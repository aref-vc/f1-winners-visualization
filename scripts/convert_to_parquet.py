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
