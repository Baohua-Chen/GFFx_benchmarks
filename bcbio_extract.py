#!/usr/bin/env python3

import argparse
import sys
from BCBio import GFF

def parse_args():
    parser = argparse.ArgumentParser(description="Extract top-level GFF features by ID")
    parser.add_argument("gff_file", help="Input GFF file")
    parser.add_argument("id_file", help="Text file with feature IDs (one per line)")
    parser.add_argument("-o", "--output", help="Output GFF file (default: stdout)", default=None)
    return parser.parse_args()

def main():
    args = parse_args()
    ids = set(line.strip() for line in open(args.id_file) if line.strip())
    output_recs = []

    with open(args.gff_file) as in_handle:
        for rec in GFF.parse(in_handle):
            selected = [f for f in rec.features if f.id in ids]
            if selected:
                rec.features = selected
                output_recs.append(rec)

    out_handle = open(args.output, "w") if args.output else sys.stdout
    GFF.write(output_recs, out_handle)
    if args.output:
        out_handle.close()

if __name__ == "__main__":
    main()
