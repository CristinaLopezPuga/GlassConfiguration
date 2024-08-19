import subprocess
import argparse
import re

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Process compounds with stoichiometric proportions.')
    parser.add_argument('file_path', type=str, help='Path to the input file containing compounds')
    return parser.parse_args()

def read_compounds(file_path):
    with open(file_path, 'r') as file:
        # Read the first line from the file
        compounds_line = file.readline().strip()
    
    # Split the line into individual compounds
    compounds = compounds_line.split()
    
    # Lists to store elements and stoichiometric proportions
    element_lists = []
    proportions_lists = []

    # Regular expression to match element symbols and their numbers
    element_pattern = re.compile(r'([A-Z][a-z]?)(\d*)')

    for compound in compounds:
        elements = []
        proportions = []

        # Find all matches in the compound
        matches = element_pattern.findall(compound)
        
        for symbol, number in matches:
            elements.append(symbol)
            proportions.append(int(number) if number else 1)
        
        # Append the lists to the result lists
        element_lists.append(elements)
        proportions_lists.append(proportions)
    
    return element_lists, proportions_lists    



# Path to the Fortran executable
fortran_executable = '/mnt/c/Users/crist/Documents/MATERIALSCIENCEANDENGINEERING/ComputationalResearch/GLASSES/Analysis_files/Mdconfig.x'


# Define the inputs required by the Fortran program
random_integer = 42   # Replace with the desired integer value for randomization
title = "Simulation Run 1"  # Replace with the desired title string

# Define the element symbols with 6 spaces between them
element_symbols = "Si     O"  # Example: Si and O with 6 spaces in between

# Define the number of ions with 6 spaces between them
number_of_ions = "28     56"  # Example: 28 and 56 with 6 spaces in between

# Define the density of the glass
glass_density = 2.45  # Replace with the desired density value

# Define the cubic unit cell answer
cubic_unit_cell = "Y"  # Replace with "Y" or "N" as needed

# Run the Fortran executable
try:
    # Start the process
    process = subprocess.Popen(
        [fortran_executable],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Provide the inputs
    input_data = f"{random_integer}\n{title}\n{element_symbols}\n{number_of_ions}\n{glass_density}\n{cubic_unit_cell}\n"
    stdout, stderr = process.communicate(input=input_data)

    # Print the output
    print("Standard Output:")
    print(stdout)

    if stderr:
        print("Standard Error:")
        print(stderr)

except subprocess.CalledProcessError as e:
    print(f"An error occurred while running the executable: {e}")
    print(f"Return Code: {e.returncode}")
    print(f"Error Output: {e.stderr}")
