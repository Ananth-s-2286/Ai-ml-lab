# Candidate Elimination Algorithm
# Dataset: EnjoySport

# Training data
training_data = [
    ["Sunny", "Warm", "Normal", "Strong", "Yes"],   # D1
    ["Sunny", "Warm", "High", "Strong", "Yes"],     # D2
    ["Rainy", "Cold", "High", "Strong", "No"],      # D3
    ["Sunny", "Warm", "High", "Weak", "Yes"]        # D4
]

# Attribute names
attributes = ["Sky", "AirTemp", "Humidity", "Wind"]

# Most Specific Boundary
S = ["Ø", "Ø", "Ø", "Ø"]

# Most General Boundary
G = [["?", "?", "?", "?"]]


# Check whether hypothesis h covers instance x
def covers(h, x):
    for i in range(len(h)):
        if h[i] != "?" and h[i] != x[i]:
            return False
    return True


# Generalize S to cover a positive example
def generalize_S(S, x):
    new_S = S.copy()

    for i in range(len(S)):
        if S[i] == "Ø":
            new_S[i] = x[i]
        elif S[i] != x[i]:
            new_S[i] = "?"

    return new_S


# Specialize G to exclude a negative example
def specialize_G(G, x, S):
    new_G = []

    # All possible values in each attribute
    domains = [
        ["Sunny", "Rainy"],
        ["Warm", "Cold"],
        ["Normal", "High"],
        ["Strong", "Weak"]
    ]

    for g in G:

        # If G does not cover the negative example,
        # it is already valid
        if not covers(g, x):
            new_G.append(g)
            continue

        # Otherwise, specialize it
        for i in range(len(g)):

            if g[i] == "?":

                for value in domains[i]:

                    if value != x[i]:

                        new_hypothesis = g.copy()
                        new_hypothesis[i] = value

                        # The specialization must be
                        # more general than S
                        if is_more_general(new_hypothesis, S):
                            new_G.append(new_hypothesis)

    return new_G


# Check whether h1 is more general than or equal to h2
def is_more_general(h1, h2):
    for i in range(len(h1)):

        if h1[i] == "?":
            continue

        if h2[i] == "Ø":
            continue

        if h1[i] != h2[i]:
            return False

    return True


# Remove duplicate hypotheses
def remove_duplicates(hypotheses):
    unique = []

    for h in hypotheses:
        if h not in unique:
            unique.append(h)

    return unique


# Remove G hypotheses that are not consistent with S
def prune_G(G, S):
    return [g for g in G if is_more_general(g, S)]


# Display a boundary
def print_boundary(boundary):
    if not boundary:
        print("{}")
    else:
        for h in boundary:
            print(h)


# -------------------------------
# Candidate Elimination Algorithm
# -------------------------------

print("CANDIDATE ELIMINATION ALGORITHM")
print("--------------------------------")

print("\nInitial Boundaries:")
print("S =", S)
print("G =", G)

for step, instance in enumerate(training_data, start=1):

    x = instance[:4]
    target = instance[4]

    print("\n====================================")
    print("Processing D" + str(step))
    print("Instance:", x)
    print("Target :", target)
    print("====================================")

    # Positive example
    if target == "Yes":

        # Remove G hypotheses that do not cover positive example
        G = [g for g in G if covers(g, x)]

        # Generalize S if required
        if not covers(S, x):
            S = generalize_S(S, x)

    # Negative example
    else:

        # Remove S if it covers the negative example
        if covers(S, x):
            S = []

        # Specialize G
        G = specialize_G(G, x, S)

        # Remove duplicate hypotheses
        G = remove_duplicates(G)

    # Display current boundaries
    print("\nAfter processing D" + str(step) + ":")

    print("S (Specific Boundary):")
    print_boundary([S] if S else [])

    print("\nG (General Boundary):")
    print_boundary(G)


# Final Version Space boundaries
print("\n\n====================================")
print("FINAL VERSION SPACE")
print("====================================")

print("\nS (Most Specific Boundary):")
print_boundary([S] if S else [])

print("\nG (Most General Boundary):")
print_boundary(G)