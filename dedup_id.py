#!/usr/bin/env python3

import re
import sys
import mmap
from tqdm import tqdm
from collections import defaultdict

def deduplicate_gff_ids(input_path, output_path):
    id_counts = defaultdict(int)
    id_map = {}

    with open(input_path, 'r') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        # å¿«éä¼°è®¡æ»è¡æ°ç¨äº tqdmï¼ä¼°å¾è¶åï¼è¿åº¦æ¡è¶å¹³æ»ï¼
        total_lines = mm.read().count(b'\n')
        mm.seek(0)  # éç½®æéå°æä»¶å¤´

        new_lines = []
        for idx, line in enumerate(tqdm(iter(mm.readline, b''), total=total_lines, desc="Processing GFF")):
            line = line.decode()
            if line.startswith('#') or not line.strip():
                new_lines.append(line)
                continue

            fields = line.strip().split('\t')
            if len(fields) != 9:
                new_lines.append(line)
                continue

            attr_str = fields[8]
            attrs = re.split(r';\s*(?=\w+=)', attr_str)
            attr_dict = dict(attr.split('=', 1) for attr in attrs if '=' in attr)

            # Update ID if duplicated
            if 'ID' in attr_dict:
                original_id = attr_dict['ID']
                id_counts[original_id] += 1
                if id_counts[original_id] > 1:
                    new_id = f"{original_id}.{id_counts[original_id]}"
                    id_map[f"{original_id}#{id_counts[original_id]}"] = new_id
                    attr_dict['ID'] = new_id
                else:
                    id_map[f"{original_id}#1"] = original_id

            # Update Parent if necessary
            if 'Parent' in attr_dict:
                parents = attr_dict['Parent'].split(',')
                new_parents = []
                for p in parents:
                    matches = [id_map[k] for k in id_map if k.startswith(p + "#")]
                    new_parents.append(matches[-1] if matches else p)
                attr_dict['Parent'] = ",".join(new_parents)

            # Rebuild attribute string
            new_attr_str = ';'.join(f"{k}={v}" for k, v in attr_dict.items())
            fields[8] = new_attr_str
            new_lines.append('\t'.join(fields) + '\n')

        mm.close()

    with open(output_path, 'w') as outfile:
        outfile.writelines(new_lines)

if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = input_file.replace('raw.', '')
        if input_file == output_file:
            output_file = output_file.replace('.gff', '.dedup.gff')
    print(input_file, output_file)
    deduplicate_gff_ids(input_file, output_file )

