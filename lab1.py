def find_lock_combinations():
    valid_combinations = []
    even_digits = [0, 2, 4, 6, 8]

    print("Searching for valid PIN combinations...\n")

    # Nested loops to check every possible 4-digit PIN made of even digits
    for d1 in even_digits:
        for d2 in even_digits:
            for d3 in even_digits:
                for d4 in even_digits:
                    
                    # Check if the sum of the digits is exactly 16
                    if (d1 + d2 + d3 + d4) == 16:
                        # Combine the digits into a 4-character string (e.g., "2446")
                        pin = f"{d1}{d2}{d3}{d4}"
                        valid_combinations.append(pin)

    # Print the results
    print(f"Found {len(valid_combinations)} matching PINs:")
    print("-" * 30)
    
    # Print them in rows of 5 for clean formatting
    for i, pin in enumerate(valid_combinations):
        print(pin, end="  ")
        if (i + 1) % 5 == 0:
            print() # Move to the next line
            
    print("\n" + "-" * 30)

# Run the function
if __name__ == "__main__":
    find_lock_combinations()