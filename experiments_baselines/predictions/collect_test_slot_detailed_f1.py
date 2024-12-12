import os
import re
import csv

metrics = {
    "loose slot f1",
    "unlabeled slot f1",
    "slot f1"
}

def extract_metrics(file_content):
    extracted_values = {}

    for metric_name in metrics:
        match = re.search(rf"^{metric_name}:(.*)", file_content, re.MULTILINE)
        if match:
            values = match.group(1).strip().split()
            extracted_values[metric_name] = values[-1] if values else None
    return extracted_values

def main():
    output_csv = "predictions/aggregated_test_slot_detailed_f1.csv"
    with open(output_csv, "w", newline="") as csvfile:
        directory = "."
        fieldnames = ["filename", "loose slot f1", "unlabeled slot f1", "slot f1"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for system in ["sidnor", "sideng", "siddial"]:
            for filename in os.listdir(directory):
                if filename.startswith("test") and filename.endswith("official.eval") and system in filename:
                    file_path = os.path.join(directory, filename)
                    with open(file_path, "r") as f:
                        file_content = f.read()
                    metrics_values = extract_metrics(file_content)
                    if metrics_values:
                        row = {
                            "filename": filename,
                            "loose slot f1": metrics_values["loose slot f1"],
                            "unlabeled slot f1": metrics_values["unlabeled slot f1"],
                            "slot f1": metrics_values["slot f1"]
                        }
                        writer.writerow(row)

if __name__ == "__main__":
    main()