import sys
import gzip
import json
import os

jsonl_directory = sys.argv[1]
text_directory = sys.argv[2]
toxic_directory = sys.argv[3]
nontoxic_directory = sys.argv[4]
threshold = 8.4

for jsonl_file in os.listdir(jsonl_directory):
    if jsonl_file.endswith('.jsonl.gz'):
        base_name = jsonl_file[:-9]  # Remove '.jsonl.gz'
        text_file_path = os.path.join(text_directory, base_name)

        if os.path.exists(text_file_path):
            with gzip.open(os.path.join(jsonl_directory, jsonl_file), 'rt', encoding='utf-8') as jf, \
                 open(text_file_path, 'r') as tf, \
                 gzip.open(os.path.join(toxic_directory, jsonl_file), 'at') as atf, \
                 gzip.open(os.path.join(nontoxic_directory, jsonl_file), 'at') as btf:

                for jsonl_line, score_line in zip(jf, tf):
                    jsonl_line = jsonl_line.strip()
                    score_line = score_line.strip()
                    score = float(score_line)
                    if score > threshold:
                        print(jsonl_line, file=atf)
                    else:
                        print(jsonl_line, file=btf)
        else:
            print(f"Warning: No corresponding text file found for {jsonl_file}: {base_name}")
