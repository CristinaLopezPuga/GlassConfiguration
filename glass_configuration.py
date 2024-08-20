import argparse
import re
import subprocess
import shutil
import os
import time
from collections import defaultdict

def read_compounds(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    compounds_line = lines[0].strip()
    compounds = compounds_line.split()
    
    molar_ratios_per_composition = []
    densities_per_composition = []
    for line in lines[1:]:
        parts = line.split()
        ratios = [float(ratio) for ratio in parts[:-1] if ratio]
        density = float(parts[-1])
        molar_ratios_per_composition.append(ratios)
        densities_per_composition.append(density)
    
    element_lists = []
    proportions_lists = []

    element_pattern = re.compile(r'([A-Z][a-z]?)(\d*)')

    for compound in compounds:
        elements = []
        proportions = []

        matches = element_pattern.findall(compound)
        
        for symbol, number in matches:
            elements.append(symbol)
            proportions.append(int(number) if number else 1)
        
        element_lists.append(elements)
        proportions_lists.append(proportions)
    
    return element_lists, proportions_lists, molar_ratios_per_composition, densities_per_composition

def calculate_atoms(total_atoms, element_lists, proportions_lists, molar_ratios_per_composition):
    compositions = []

    for molar_ratios in molar_ratios_per_composition:
        element_counts = defaultdict(float)

        for elements, proportions, mole_fraction in zip(element_lists, proportions_lists, molar_ratios):
            num_atoms_compound = mole_fraction * total_atoms
            total_proportions = sum(proportions)
            
            for element, proportion in zip(elements, proportions):
                element_atoms = num_atoms_compound * (proportion / total_proportions)
                element_counts[element] += element_atoms

        compositions.append({element: round(count) for element, count in element_counts.items()})

    return compositions

def run_fortran_executable(composition, fortran_executable, total_atoms, density, random_integer=42, title="Simulation Run 1", cubic_unit_cell="Y"):
    # Prepare the element symbols and number of ions
    element_symbols = " ".join(f"{elem:6}" for elem in composition.keys())
    number_of_ions = " ".join(f"{int(count):6}" for count in composition.values())
    
    # Create a unique name for the output file using the current time
    timestamp = time.strftime("%H%M%S")  # Format time as HourMinuteSecond
    unique_filename = f"lammps-in_{timestamp}.dat"
    
    # Run the Fortran executable
    try:
        process = subprocess.Popen(
            [fortran_executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Provide the inputs
        input_data = f"{random_integer}\n{title}\n{element_symbols}\n{number_of_ions}\n{density}\n{cubic_unit_cell}\n"
        stdout, stderr = process.communicate(input=input_data)

        # Print the output
        print("Standard Output:")
        print(stdout)

        if stderr:
            print("Standard Error:")
            print(stderr)

        # Rename the output file to a unique name
        shutil.move('lammps-in.dat', unique_filename)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the executable: {e}")
        print(f"Return Code: {e.returncode}")
        print(f"Error Output: {e.stderr}")


def parse_args():
    parser = argparse.ArgumentParser(description='Process compounds with stoichiometric proportions.')
    parser.add_argument('file_path', type=str, help='Path to the input file containing compounds')
    parser.add_argument('total_atoms', type=int, help='Total number of atoms in the glass')
    parser.add_argument('fortran_executable', type=str, help='Path to the Fortran executable')
    return parser.parse_args()

def main():
    args = parse_args()
    
    element_lists, proportions_lists, molar_ratios_per_composition, densities_per_composition = read_compounds(args.file_path)
    compositions = calculate_atoms(args.total_atoms, element_lists, proportions_lists, molar_ratios_per_composition)
    
    for i, (composition, density) in enumerate(zip(compositions, densities_per_composition), 1):
        print(f"\nRunning Fortran executable for Composition {i}:")
        run_fortran_executable(composition, args.fortran_executable, args.total_atoms, density)

if __name__ == "__main__":
    main()
