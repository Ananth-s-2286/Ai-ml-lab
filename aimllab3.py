# Find-S Algorithm
# AI & ML Lab Practical

import csv

# Read dataset from CSV file
data = []

with open("workload_data.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header
    for row in reader:
        data.append(row)

# Initialize hypothesis as None
hypothesis = None

print("Find-S Algorithm Execution\n")

# Process each training example
for i, row in enumerate(data):

    # Attributes (excluding target class)
    attributes = row[:-1]

    # Target class
    target = row[-1]

    print(f"Processing Row {i+1}: {row}")

    # Consider only positive examples
    if target == "Yes":

        # First positive example initializes hypothesis
        if hypothesis is None:
            hypothesis = attributes.copy()

        else:
            # Compare each attribute
            for j in range(len(hypothesis)):
                if hypothesis[j] != attributes[j]:
                    hypothesis[j] = "?"

        print("Updated Hypothesis:", hypothesis)

    else:
        print("Negative example ignored.")

    print("-" * 60)

print("\nFinal Specific Hypothesis:")
print(hypothesis)