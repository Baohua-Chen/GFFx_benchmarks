#!/usr/bin/env python

import sys
import struct
from pathlib import Path

def print_rit_file(rit_path: Path):
    """Print the contents of a .rit file (binary intervals data)"""
    print(f"\nContents of {rit_path}:")
    try:
        with open(rit_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File not found: {rit_path}")
        return

    # Each entry is 12 bytes: start(u32), end(u32), gof_id(u32)
    entry_format = "<III"  # Little-endian, 3 unsigned 32-bit integers
    entry_size = struct.calcsize(entry_format)
    
    if len(data) % entry_size != 0:
        print(f"Warning: File size {len(data)} is not a multiple of {entry_size} (corrupted?)")
    
    for i in range(0, len(data), entry_size):
        entry = data[i:i+entry_size]
        start, end, gof_id = struct.unpack(entry_format, entry)
        print(f"Interval {i//entry_size}: start={start}, end={end}, gof_id={gof_id}")

def print_rix_file(rix_path: Path, sqs_path: Path, rit_path: Path):
    """Print the contents of a .rix file (index) with seqid names"""
    print(f"\nContents of {rix_path}:")
    
    # Read seqids from .sqs file
    with open(sqs_path, "r") as f:
        seqids = [line.strip() for line in f if line.strip()]
    
    # Read .rix file
    with open(rix_path, "rb") as f:
        data = f.read()
    
    # Verify file size
    if len(data) != (len(seqids) + 1) * 4:
        print(f"Warning: Expected {(len(seqids)+1)*4} bytes, got {len(data)}")
    
    # Parse offsets
    offsets = []
    for i in range(0, len(data), 4):
        offset = int.from_bytes(data[i:i+4], byteorder='little')
        offsets.append(offset)
    
    # Get total intervals from .rit file
    rit_size = rit_path.stat().st_size
    total_intervals = rit_size // 12
    
    print(f"{'SeqID':<15} | {'Index':<5} | {'Offset':<10} | {'End (calc)':<10}")
    print("-" * 50)
    
    for i in range(len(offsets)-1):  # æåä¸ä¸ªæ¯ç»ææ è®°
        seqid = seqids[i] if i < len(seqids) else f"UNKNOWN_{i}"
        offset = offsets[i]
        end = offsets[i+1] if i+1 < len(offsets) else total_intervals * 12
        
        # Convert end to interval count for last line
        display_end = end if i+1 < len(offsets) else total_intervals
        print(f"{seqid:<15} | {i:<5} | {offset:<10} | {display_end:<10}")   

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <gff_base_path>")
        sys.exit(1)

    gff_file = sys.argv[1]
    
    # File paths
    rit_path = Path(gff_file + ".rit")
    rix_path = Path(gff_file + ".rix")
    sqs_path = Path(gff_file + ".sqs")
    
    print_rit_file(rit_path)
    
    if rix_path.exists() and sqs_path.exists():
        print_rix_file(rix_path, sqs_path, rit_path)
    else:
        missing = [f for f in [rix_path, sqs_path] if not f.exists()]
        print(f"Missing files: {missing}")
