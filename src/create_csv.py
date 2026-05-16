import os
import csv

folder = "dataset"
output_file = "gesture_data.csv"

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            label = file.split("_")[0]

            with open(os.path.join(folder, file), "r") as f:
                values = f.read().split(",")

            # Add label at end
            row = values + [label]
            writer.writerow(row)

print("CSV file created successfully without pandas!")