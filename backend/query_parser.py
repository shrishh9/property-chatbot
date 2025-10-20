import re
from typing import Dict, List, Optional

class QueryParser:
    """Parse natural language queries for real estate search"""
    
    def __init__(self):
        self.bhk_pattern = r'(\d+)\s*(?:bhk|BHK|Bhk)'
        self.price_patterns = [
            r'(?:under|below|less than|upto|up to)\s*₹?\s*([\d.]+)\s*(cr|crore|lakh|l|lakhs)',
            r'₹?\s*([\d.]+)\s*(cr|crore|lakh|l|lakhs)',
        ]
        self.status_keywords = {
            'ready': ['ready', 'ready to move', 'ready-to-move', 'immediate'],
            'construction': ['under construction', 'upcoming', 'pre-launch', 'construction']
        }
        self.cities = ['pune', 'mumbai', 'bangalore', 'delhi', 'hyderabad', 'chennai', 'chembur', 'wakad', 'baner']
        
    def parse_query(self, query: str) -> Dict:
        """
        Parse user query and extract filters
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with extracted filters
        """
        query_lower = query.lower()
        filters = {}
        
        # Extract BHK
        bhk_match = re.search(self.bhk_pattern, query, re.IGNORECASE)
        if bhk_match:
            filters['bhk'] = f"{bhk_match.group(1)}BHK"
        
        # Extract price
        price = self._extract_price(query_lower)
        if price:
            filters['max_price'] = price
        
        # Extract city/location
        city = self._extract_city(query_lower)
        if city:
            filters['city'] = city
        
        # Extract status
        status = self._extract_status(query_lower)
        if status:
            filters['status'] = status
        
        # Extract property type
        if 'office' in query_lower or 'commercial' in query_lower:
            filters['property_type'] = 'commercial'
        elif 'villa' in query_lower or 'house' in query_lower:
            filters['property_type'] = 'villa'
        else:
            filters['property_type'] = 'residential'
        
        return filters
    
    def _extract_price(self, query: str) -> Optional[float]:
        """Extract price from query and convert to rupees"""
        for pattern in self.price_patterns:
            match = re.search(pattern, query)
            if match:
                amount = float(match.group(1))
                unit = match.group(2).lower()
                
                if 'cr' in unit or 'crore' in unit:
                    return amount * 10000000  # Convert crores to rupees
                elif 'l' in unit or 'lakh' in unit:
                    return amount * 100000  # Convert lakhs to rupees
        return None
    
    def _extract_city(self, query: str) -> Optional[str]:
        """Extract city name from query"""
        for city in self.cities:
            if city in query:
                return city.capitalize()
        return None
    
    def _extract_status(self, query: str) -> Optional[str]:
        """Extract property status from query"""
        for status, keywords in self.status_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return 'READY_TO_MOVE' if status == 'ready' else 'UNDER_CONSTRUCTION'
        return None
