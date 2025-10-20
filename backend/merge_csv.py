import pandas as pd
import os

print("Starting CSV merge process...")

# Read all CSV files
print("\n1. Reading CSV files...")
project_df = pd.read_csv('data/project.csv')
config_df = pd.read_csv('data/ProjectConfiguration.csv')
variant_df = pd.read_csv('data/ProjectConfigurationVariant.csv')
address_df = pd.read_csv('data/ProjectAddress.csv')

print(f"   ✓ Project: {len(project_df)} rows")
print(f"   ✓ Config: {len(config_df)} rows")
print(f"   ✓ Variant: {len(variant_df)} rows")
print(f"   ✓ Address: {len(address_df)} rows")

# Merge the dataframes
print("\n2. Merging dataframes...")
merged_df = project_df.merge(config_df, left_on='id', right_on='projectId', how='left', suffixes=('', '_config'))
merged_df = merged_df.merge(variant_df, left_on='id_config', right_on='configurationId', how='left', suffixes=('', '_variant'))
merged_df = merged_df.merge(address_df, left_on='id', right_on='projectId', how='left', suffixes=('', '_address'))

# Select relevant columns
final_columns = [
    'projectName', 'status', 'type', 'carpetArea', 'price', 'balcony', 
    'bathrooms', 'furnishedType', 'landmark', 'fullAddress', 'pincode',
    'slug', 'possessionDate', 'listingType', 'floorPlanImage'
]

final_df = merged_df[final_columns].copy()
final_df['price'] = pd.to_numeric(final_df['price'], errors='coerce')

# Save merged file
print("\n3. Saving merged file...")
final_df.to_csv('data/merged_properties.csv', index=False)

print(f"\n✅ SUCCESS! Created data/merged_properties.csv")
print(f"   Total rows: {len(final_df)}")
print(f"   Columns: {', '.join(final_df.columns)}")
print(f"\n   Sample data:")
print(final_df[['projectName', 'type', 'price', 'status']].head(5))

