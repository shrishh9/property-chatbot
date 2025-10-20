import pandas as pd
from typing import Dict, List
import re

class PropertySearch:
    """Search properties from CSV data based on filters"""
    
    def __init__(self, csv_path: str = 'data/merged_properties.csv'):
        """Initialize with property data"""
        self.df = pd.read_csv(csv_path)
        self._clean_data()
    
    def _clean_data(self):
        """Clean and prepare data"""
        # Convert price to numeric
        self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')
        
        # Fill NaN values
        self.df['type'] = self.df['type'].fillna('Unknown')
        self.df['status'] = self.df['status'].fillna('Unknown')
        self.df['landmark'] = self.df['landmark'].fillna('Not specified')
        
    def search(self, filters: Dict) -> List[Dict]:
        """
        Search properties based on filters
        
        Args:
            filters: Dictionary with search filters
            
        Returns:
            List of matching properties
        """
        df_filtered = self.df.copy()
        
        # Apply BHK filter
        if 'bhk' in filters:
            df_filtered = df_filtered[df_filtered['type'] == filters['bhk']]
        
        # Apply price filter
        if 'max_price' in filters:
            df_filtered = df_filtered[df_filtered['price'] <= filters['max_price']]
        
        # Apply status filter
        if 'status' in filters:
            df_filtered = df_filtered[df_filtered['status'] == filters['status']]
        
        # Apply city filter (search in landmark and fullAddress)
        if 'city' in filters:
            city_mask = (
                df_filtered['landmark'].str.contains(filters['city'], case=False, na=False) |
                df_filtered['fullAddress'].str.contains(filters['city'], case=False, na=False)
            )
            df_filtered = df_filtered[city_mask]
        
        # Convert to list of dictionaries
        results = []
        for _, row in df_filtered.iterrows():
            property_dict = {
                'title': row['projectName'],
                'type': row['type'],
                'price': self._format_price(row['price']),
                'price_raw': row['price'],
                'carpet_area': f"{row['carpetArea']} sq.ft" if pd.notna(row['carpetArea']) else 'N/A',
                'location': row['landmark'],
                'full_address': row['fullAddress'] if pd.notna(row['fullAddress']) else 'Address not available',
                'status': self._format_status(row['status']),
                'bathrooms': int(row['bathrooms']) if pd.notna(row['bathrooms']) else 'N/A',
                'balcony': int(row['balcony']) if pd.notna(row['balcony']) else 0,
                'furnished': row['furnishedType'] if pd.notna(row['furnishedType']) else 'Not specified',
                'possession': row['possessionDate'] if pd.notna(row['possessionDate']) else 'Not specified',
                'slug': row['slug'] if pd.notna(row['slug']) else '#',
                'image': row['floorPlanImage'] if pd.notna(row['floorPlanImage']) else None
            }
            results.append(property_dict)
        
        return results
    
    def _format_price(self, price: float) -> str:
        """Format price in Indian currency format"""
        if pd.isna(price):
            return 'Price on request'
        
        if price >= 10000000:  # Crores
            return f"₹{price/10000000:.2f} Cr"
        elif price >= 100000:  # Lakhs
            return f"₹{price/100000:.2f} L"
        else:
            return f"₹{price:,.0f}"
    
    def _format_status(self, status: str) -> str:
        """Format status for display"""
        if status == 'READY_TO_MOVE':
            return 'Ready to Move'
        elif status == 'UNDER_CONSTRUCTION':
            return 'Under Construction'
        return status
    
    def generate_summary(self, results: List[Dict], filters: Dict) -> str:
        """
        Generate natural language summary of search results
        
        Args:
            results: List of property results
            filters: Original search filters
            
        Returns:
            Summary string
        """
        if not results:
            return self._generate_no_results_summary(filters)
        
        count = len(results)
        bhk_type = filters.get('bhk', 'properties')
        city = filters.get('city', 'your area')
        
        # Calculate statistics
        prices = [r['price_raw'] for r in results if r['price_raw'] > 0]
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            price_range = f"₹{min_price/10000000:.2f} Cr to ₹{max_price/10000000:.2f} Cr"
        else:
            price_range = "various price points"
        
        # Count by status
        ready_count = sum(1 for r in results if 'Ready' in r['status'])
        construction_count = count - ready_count
        
        # Count unique locations
        locations = list(set([r['location'] for r in results if r['location'] != 'Not specified']))
        top_locations = ', '.join(locations[:3]) if locations else city
        
        # Generate summary
        summary = f"Found {count} {bhk_type} {'property' if count == 1 else 'properties'} in {city}. "
        summary += f"Prices range from {price_range}. "
        
        if ready_count > 0:
            summary += f"{ready_count} {'is' if ready_count == 1 else 'are'} ready to move. "
        
        if construction_count > 0:
            summary += f"{construction_count} under construction. "
        
        summary += f"Popular locations include {top_locations}."
        
        return summary
    
    def _generate_no_results_summary(self, filters: Dict) -> str:
        """Generate summary when no results found"""
        bhk = filters.get('bhk', 'properties')
        city = filters.get('city', 'this location')
        
        # Try to suggest alternatives
        summary = f"No {bhk} properties found matching your exact criteria in {city}. "
        
        # Search without price filter
        relaxed_filters = {k: v for k, v in filters.items() if k != 'max_price'}
        alternative_results = self.search(relaxed_filters)
        
        if alternative_results:
            summary += f"However, {len(alternative_results)} properties are available if you adjust your budget. "
        else:
            summary += "Try exploring nearby areas or different configurations."
        
        return summary
