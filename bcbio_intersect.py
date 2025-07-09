#!/usr/bin/env python3

import argparse
import sys
from BCBio import GFF
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="Extract GFF features overlapping BED regions")
    parser.add_argument("gff_file", help="Input GFF file")
    parser.add_argument("bed_file", help="BED file (only first 3 columns used)")
    parser.add_argument("-o", "--output", help="Output GFF file (default: stdout)", default=None)
    return parser.parse_args()

def load_bed_regions(bed_file):
    regions = defaultdict(list)
    with open(bed_file) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            chrom, start, end = line.strip().split()[:3]
            regions[chrom].append((int(start), int(end)))
    return regions

def overlaps(start1, end1, start2, end2):
    return not (end1 <= start2 or end2 <= start1)

def main():
    args = parse_args()
    bed_regions = load_bed_regions(args.bed_file)
    output_recs = []

    with open(args.gff_file) as in_handle:
        for rec in GFF.parse(in_handle):
            chrom = rec.id
            if chrom not in bed_regions:
                continue
            selected = []
            for feat in rec.features:
                f_start = int(feat.location.start)
                f_end = int(feat.location.end)
                for b_start, b_end in bed_regions[chrom]:
                    if overlaps(f_start, f_end, b_start, b_end):
                        selected.append(feat)
                        break
            if selected:
                rec.features = selected
                output_recs.append(rec)

    out_handle = open(args.output, "w") if args.output else sys.stdout
    GFF.write(output_recs, out_handle)
    if args.output:
        out_handle.close()

if __name__ == "__main__":
    main()
