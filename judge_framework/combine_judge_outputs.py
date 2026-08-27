import os
import json
import argparse
import csv
from typing import List, Dict

def find_judge_output_files(base_folder: str) -> List[str]:
    files = []
    for entry in os.listdir(base_folder):
        subfolder = os.path.join(base_folder, entry)
        if os.path.isdir(subfolder) and entry.isdigit():
            judge_file = os.path.join(subfolder, 'judge_output.json')
            if os.path.isfile(judge_file):
                files.append(judge_file)
    return files

def parse_judge_output(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Attach pid if not present
    if 'pid' not in data:
        # Try to infer pid from folder name
        pid = os.path.basename(os.path.dirname(file_path))
        data['pid'] = pid
    return data

def load_attack_evaluations(attack_json_path: str) -> Dict:
    """Load attack evaluation json and return a dict mapping pid to (verdict, reasoning)."""
    with open(attack_json_path, 'r', encoding='utf-8') as f:
        attack_data = json.load(f)
    pid_to_attack = {}
    for item in attack_data:
        pid = str(item.get('pid'))
        evaluation = item.get('evaluation')
        reasoning = item.get('reasoning')
        if pid is not None and evaluation is not None:
            pid_to_attack[pid] = {
                'verdict': evaluation,
                'reasoning': reasoning
            }
    return pid_to_attack

def load_refusal_evaluations(refusal_json_path: str) -> Dict:
    """Load refusal evaluation json and return a dict mapping pid to (verdict, reasoning)."""
    with open(refusal_json_path, 'r', encoding='utf-8') as f:
        refusal_data = json.load(f)
    pid_to_refusal = {}
    for item in refusal_data:
        pid = str(item.get('pid'))
        evaluation = item.get('evaluation')
        reasoning = item.get('reasoning')
        if pid is not None and evaluation is not None:
            pid_to_refusal[pid] = {
                'verdict': evaluation,
                'reasoning': reasoning
            }
    return pid_to_refusal

def load_malicious_categories(csv_path: str) -> Dict:
    """Load malicious categories from a CSV file and return a dict mapping pid to category."""
    pid_to_category = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = str(row.get('pid'))
            category = row.get('malicious categories')
            if pid and category:
                pid_to_category[pid] = category
    return pid_to_category

def main():
    parser = argparse.ArgumentParser(description='Combine judge model verdicts from multiple subfolders and attack evaluation json.')
    parser.add_argument('folder', type=str, help='Path to the folder containing pid subfolders with judge_output.json files')
    parser.add_argument('--output', type=str, default='combined_judge_results.json', help='Output JSON file name')
    parser.add_argument('--attack_evaluation_json', type=str, required=False, help='Path to attack evaluation json file')
    parser.add_argument('--refusal_evaluation_json', type=str, required=False, help='Path to refusal evaluation json file')
    parser.add_argument(
        '--malicious_category_csv',
        type=str,
        default=None,
        help='Optional path to a CSV containing pid and malicious categories columns',
    )
    args = parser.parse_args()

    base_folder = args.folder
    output_file = args.output
    attack_json_path = args.attack_evaluation_json
    refusal_json_path = args.refusal_evaluation_json
    malicious_category_csv = args.malicious_category_csv

    judge_files = find_judge_output_files(base_folder)
    if not judge_files:
        print(f'No judge_output.json files found in {base_folder}')
        return

    # Collect all unique pids from both sources
    pids_from_judge = set()
    judge_results_by_pid = {}
    for file_path in sorted(judge_files):
        try:
            result = parse_judge_output(file_path)
            pid = str(result.get('pid'))
            pids_from_judge.add(pid)
            judge_results_by_pid[pid] = result
        except Exception as e:
            print(f'Error reading {file_path}: {e}')

    pids_from_attack = set()
    pid_to_attack = {}
    if attack_json_path:
        pid_to_attack = load_attack_evaluations(attack_json_path)
        pids_from_attack = set(pid_to_attack.keys())

    pid_to_refusal = {}
    if refusal_json_path:
        pid_to_refusal = load_refusal_evaluations(refusal_json_path)

    pid_to_category = {}
    if malicious_category_csv:
        pid_to_category = load_malicious_categories(malicious_category_csv)

    all_pids = sorted(pids_from_judge | pids_from_attack | set(pid_to_refusal.keys()), key=lambda x: int(x) if x.isdigit() else x)

    combined_results = []
    for pid in all_pids:
        new_result = {'pid': pid}
        category = pid_to_category.get(pid)
        if category:
            new_result['malicious_category'] = category
        attack = pid_to_attack.get(pid)
        if attack:
            new_result['successful_attack'] = attack
        refusal = pid_to_refusal.get(pid)
        if refusal:
            new_result['refusal'] = refusal
        judge_result = judge_results_by_pid.get(pid)
        if judge_result:
            for k, v in judge_result.items():
                if k not in ('pid', 'successful_attack', 'refusal', 'malicious_category'):
                    new_result[k] = v
        combined_results.append(new_result)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=4, ensure_ascii=False)
    print(f'Combined results saved to {output_file}')

if __name__ == '__main__':
    main()
