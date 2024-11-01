import argparse
import sys
import gzip
import os

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process a single JSONL file by classifying its entries as toxic or non-toxic based on scores.'
    )
    
    # Positional arguments
    parser.add_argument(
        'jsonl_directory',
        type=str,
        help='Directory containing .jsonl.gz files'
    )
    parser.add_argument(
        'score_directory',
        type=str,
        help='Directory containing score files corresponding to JSONL files'
    )
    parser.add_argument(
        'toxic_directory',
        type=str,
        help='Directory to save toxic texts'
    )
    parser.add_argument(
        'nontoxic_directory',
        type=str,
        help='Directory to save non-toxic texts'
    )
    
    # Optional argument for threshold with default value
    parser.add_argument(
        '--threshold',
        type=float,
        default=8.4,
        help='Threshold for classifying toxicity (default: 8.4)'
    )
    
    # Required argument to specify a single file to process
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Specify a single .jsonl.gz file to process'
    )
    
    return parser.parse_args()

def process_file(jsonl_file, args):
    base_name = os.path.splitext(os.path.splitext(jsonl_file)[0])[0] + '.txt'  # Remove '.jsonl.gz' and add '.txt'
    score_file_path = os.path.join(args.score_directory, base_name)
    
    if not os.path.exists(score_file_path):
        print(f"Warning: No corresponding score file found for {jsonl_file}: {base_name}", file=sys.stderr)
        return
    
    jsonl_path = os.path.join(args.jsonl_directory, jsonl_file)
    toxic_path = os.path.join(args.toxic_directory, jsonl_file)
    nontoxic_path = os.path.join(args.nontoxic_directory, jsonl_file)
    
    try:
        with gzip.open(jsonl_path, 'rt', encoding='utf-8') as jf, \
             open(score_file_path, 'r', encoding='utf-8') as sf, \
             gzip.open(toxic_path, 'at', encoding='utf-8') as tf, \
             gzip.open(nontoxic_path, 'at', encoding='utf-8') as ntf:
            
            for jsonl_line, score_line in zip(jf, sf):
                jsonl_line = jsonl_line.strip()
                score_line = score_line.strip()
                
                # Skip empty lines
                if not jsonl_line or not score_line:
                    continue
                
                try:
                    score = float(score_line)
                except ValueError:
                    print(f"Warning: Invalid score '{score_line}' in file {score_file_path}", file=sys.stderr)
                    continue
                
                if score > args.threshold:
                    print(jsonl_line, file=tf)
                else:
                    print(jsonl_line, file=ntf)
    
    except Exception as e:
        print(f"Error processing file {jsonl_file}: {e}", file=sys.stderr)

def main():
    args = parse_arguments()
    
    # Ensure output directories exist
    os.makedirs(args.toxic_directory, exist_ok=True)
    os.makedirs(args.nontoxic_directory, exist_ok=True)
    
    jsonl_file = args.file
    
    # Validate the specified file
    if not jsonl_file.endswith('.jsonl.gz'):
        print(f"Error: Specified file '{jsonl_file}' does not have a '.jsonl.gz' extension.", file=sys.stderr)
        sys.exit(1)
    
    jsonl_path = os.path.join(args.jsonl_directory, jsonl_file)
    if not os.path.isfile(jsonl_path):
        print(f"Error: Specified file '{jsonl_file}' does not exist in {args.jsonl_directory}.", file=sys.stderr)
        sys.exit(1)
    
    # Process the specified file
    process_file(jsonl_file, args)

if __name__ == '__main__':
    main()

