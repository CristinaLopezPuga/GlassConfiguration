import pandas as pd
import argparse

# Define constants
molecular_weights = {
    'SiO2': 60.08, 'Na2O': 61.98, 'Al2O3': 101.96, 'B2O3': 69.62, 'Li2O': 29.88,
    'K2O': 94.20, 'MgO': 40.30, 'CaO': 56.08, 'Fe2O3': 159.69, 'TiO2': 79.87,
    'ZnO': 81.38, 'ZrO2': 123.22, 'BaO': 153.33, 'MnO': 70.94, 'SrO': 103.62,
    'PbO': 223.20, 'Sb2O3': 291.50, 'P2O5': 141.94, 'WO3': 231.84, 'ThO2': 264.04,
    'Bi2O3': 465.96, 'CdO': 128.41, 'Cr2O3': 151.99, 'F': 18.998, 'NiO': 74.69, 
    'SO3': 80.06, 'Cs2O': 281.81, 'CuO': 79.55, 'MoO3': 143.94, 'Nd2O3': 336.48, 
    'RuO2': 133.07,
}

packing_densities = {
    'SiO2': 13.9e-6, 'Na2O': 12.3e-6, 'Al2O3': 21.15e-6, 'B2O3': 20.8e-6, 'Li2O': 9.0e-6,
    'K2O': 20.2e-6, 'MgO': 7.9e-6, 'CaO': 9.4e-6, 'Fe2O3': 22.1e-6, 'TiO2': 14.4e-6,
    'ZnO': 8.0e-6, 'ZrO2': 14.8e-6, 'BaO': 13.3e-6, 'MnO': 14.2e-6, 'SrO': 10.6e-6,
    'PbO': 11.1e-6, 'Sb2O3': 23.0e-6, 'P2O5': 34.6e-6, 'WO3': 21.3e-6, 'ThO2': 16.4e-6,
    'Bi2O3': 26.1e-6, 'CdO': 9.1e-6, 'Cr2O3': 21.9e-6, 'F': 11.1e-6, 'NiO': 11.1e-6, 
    'SO3': 11.1e-6, 'Cs2O': 31.7e-6, 'CuO': 7.9e-6, 'MoO3': 21.3e-6, 'Nd2O3': 25.6e-6, 
    'RuO2': 11.1e-6,
}

def calculate_density(molecular_weights, packing_densities, composition):
    numerator = sum(molecular_weights[comp] * composition[comp] for comp in composition)
    denominator = sum(packing_densities[comp] * composition[comp] for comp in composition)
    density_kg_m3 = 0.53 * (numerator / denominator)
    density_g_cm3 = density_kg_m3 * 0.000001
    return density_g_cm3

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Calculate density from composition data in a CSV file.')
    parser.add_argument('input_csv', type=str, help='Path to the input CSV file')

    # Parse the arguments
    args = parser.parse_args()
    csv_file_path = args.input_csv

    # Read the composition data from the CSV file
    df = pd.read_csv(csv_file_path)

    # Calculate density for each composition
    densities = []
    for index, row in df.iterrows():
        # Create a dictionary for the composition of the current row
        composition = {comp: row[comp] for comp in molecular_weights.keys() if comp in row and not pd.isna(row[comp])}
        
        # Calculate density and append to the list
        density = calculate_density(molecular_weights, packing_densities, composition)
        densities.append(density)

    # Add the densities to the DataFrame as a new column
    df['Density (g/cm^3)'] = densities

    # Save the updated DataFrame back to the same CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"Density calculations completed. Results saved in the same file: {csv_file_path}.")

if __name__ == '__main__':
    main()

