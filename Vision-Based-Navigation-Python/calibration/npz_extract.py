import numpy as np

def load_and_display_npz(file_path):
    """
    Load an .npz file, display its keys, and print the contents of each array.
    """
    try:
        # Load the .npz file
        data = np.load(file_path)
        
        # List all arrays in the file
        print(f"Arrays in {file_path}: {data.files}")
        
        # Access and display each array
        for key in data.files:
            print(f"\nArray '{key}':\n{data[key]}")
        
        # Close the file
        data.close()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'example.npz' with the path to your .npz file
    file_path = 'calibration.npz'
    load_and_display_npz(file_path)
