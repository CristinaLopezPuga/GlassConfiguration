import subprocess

# Path to the Fortran executable
fortran_executable = "./your_fortran_executable"

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
