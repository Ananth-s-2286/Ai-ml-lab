# ID3 Play Tennis Decision Tree

A small Python implementation of the ID3 algorithm using the classic 14-row Play Tennis dataset.

## Run

```bash
python3 id3_tennis.py
```

The program prints:

- Dataset entropy
- Information gain for each root attribute
- The generated decision tree
- Training accuracy

No third-party packages are required.

## Result

The learned tree uses `Outlook` as its root:

- `Overcast` -> `Yes`
- `Sunny` -> split on `Humidity`
- `Rain` -> split on `Wind`
