import pandas as pd
import requests
from io import StringIO

def decode_secret_message(source):
    try:
        # Load HTML tables from a URL or local file based on the provided source
        if source.startswith(('http://', 'https://')):
            response = requests.get(source)
            response.raise_for_status()
            tables = pd.read_html(StringIO(response.text))
        else:
            tables = pd.read_html(source)
    except Exception as e:
        print(f"Error fetching or parsing HTML data: {e}")
        return

    if not tables:
        print("No tables found in the provided HTML source.")
        return

    df = tables[0]

    # Explicitly check if the first row is a header by confirming expected numeric columns
    # (x and y coordinates) contain non-integer values, indicating headers instead of data
    first_row = df.iloc[0]
    header_present = not (
        str(first_row[0]).isdigit() and str(first_row[2]).isdigit()
    )

    try:
        # Extract coordinates and characters, skipping the header row if detected
        data_start_idx = 1 if header_present else 0
        coordinates = [
            (char, int(x), int(y))
            for x, char, y in df.iloc[data_start_idx:].itertuples(index=False, name=None)
        ]
    except ValueError as e:
        # Handle unexpected failures in converting coordinates to integers
        print(f"Error converting coordinate values to integers: {e}")
        return

    if not coordinates:
        print("No valid coordinate data found after processing.")
        return

    # Determine grid size based on maximum coordinate values
    grid_width = max(coord[1] for coord in coordinates) + 1
    grid_height = max(coord[2] for coord in coordinates) + 1

    # Initialize the grid with blank spaces
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

    # Populate the grid with characters at specified coordinates
    for char, x, y in coordinates:
        grid[y][x] = char

    # Display the grid visually as the decoded secret message
    print("\n".join(''.join(row) for row in grid))

if __name__ == "__main__":
    source = r"https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub?output=txt"  # Replace with URL or file path
    decode_secret_message(source)
