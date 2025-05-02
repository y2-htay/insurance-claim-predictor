import os
import pickle

def describe_object(obj):
    lines = []
    lines.append(f"Type: {type(obj)}\n")

    if hasattr(obj, 'get_params'):
        lines.append("Model Parameters:")
        try:
            for k, v in obj.get_params().items():
                lines.append(f"  {k}: {v}")
        except Exception as e:
            lines.append(f"  (Error reading parameters: {e})")

    if hasattr(obj, 'feature_importances_'):
        lines.append("\nFeature Importances:")
        try:
            importances = obj.feature_importances_
            lines.extend([f"  {i}: {val}" for i, val in enumerate(importances)])
        except Exception as e:
            lines.append(f"  (Error reading importances: {e})")

    if isinstance(obj, dict):
        lines.append("\nDictionary Keys:")
        for k in obj:
            lines.append(f"  {k} → {type(obj[k])}")
    
    return '\n'.join(lines)

def process_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            obj = pickle.load(f)

        description = describe_object(obj)
        output_path = file_path.replace('.pkl', '_info.txt')

        
        with open(output_path, 'w', encoding='utf-8') as f:

            f.write(description)

        print(f"✓ Info saved: {output_path}")
    except Exception as e:
        print(f"✗ Failed to process {file_path}: {e}")

def find_and_process_all_pkls(root_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.pkl'):
                full_path = os.path.join(root, file)
                process_pickle_file(full_path)


find_and_process_all_pkls('AI-Stuff/Yamin')
