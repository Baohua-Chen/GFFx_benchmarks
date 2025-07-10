# Benchmarking Scripts and Datasets for GFFx

This directory contains benchmarking scripts and datasets used to evaluate the performance of **GFFx** and other GFF/GTF tools on large-scale feature extraction and region-based queries.

It is designed to generate **reproducible, large-scale performance comparisons** among tools, including:

- [`GFFx`](https://github.com/Baohua-Chen/GFFx)
- `gffutils`
- `gffread`
- `agat`
- `bedtools`
- `bcbio-gff`

---

## Contents

```text
benchmark/
├── run_benchmark.s# Entry point: runs index, extract, and intersect benchmarking
├── benchmark.sh         # Core driver script for perforbenchmarking
├── extract/             # Stores generated inputs & logs for feature extraction
├── intersect/           # Stores generated inputs & logs for region intersection
├── LICENSE-MIT          # License for scripts
├── LICENSE-CC-BY        # License for benchmark data
└── README.md            # This file
```

---

## How to Use

### Step 1: Prepare GFF & FASTA index files

Make sure files like `at.gff` and `at.fa.fai` exist in the working directory.

### Step 2: Run the full benchmark

```bash
bash run_benchmark.sh
```

This will:
- Run index generation using multiple tools
- Generate 100 input files per task
- Benchmark extract & intersect using different tools per datas
- Save timing logs to structured folders

---

## Output Structure

After running `benchmark.sh`, results will be organized as:

```
extract/
  └── at/
      └── gffx/
          ├── input_001.txt
          └── run_001.log
intersect/
  └── dm/
      └── gffutils/
          ├── input_087.txt
          └── run_087.log
```

Each `run_*.log` contains `/usr/bin/time -v` output with memory and runtime metrics.

---

## License

This directory uses **dual licensing** for clarity:

- **Scripts** (`*.sh`, `*.py`, and `*.ipynb`) are licensed under the [MIT License](./LICENSE-MIT)
- **Benchmark datasets** (all other type of files except "Scripts") are licensed under the [Creative Commons Attribution 4.0 (CC-BY 4.0)](./LICENSE-CC-BY)

> Please cite the GFFx project or this repository if you use the benchmark data in research or publications.

---

## Author

Created by [Baohua Chen](https://github.com/Baohua-Chen), 2025  
For questions, please file an issue on the [GFFx GitHub repo](https://github.com/Baohua-Chen/GFFx/issues).
