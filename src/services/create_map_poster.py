"""
Wrapper module for the web API to use the upstream create_map_poster functionality.
This bridges the old src/services structure with the new root-level implementation.
"""
import sys
import os
from pathlib import Path

# Add the root directory to the Python path so we can import the upstream module
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import from the upstream create_map_poster.py
from create_map_poster import (
    create_poster as upstream_create_poster,
    generate_output_filename,
    list_themes,
    get_available_themes,
    load_theme,
)

# Use local geocoding with diskcache (better for the web API)
from services.geocoding import get_coordinates

# Re-export POSTERS_DIR for compatibility with the API
from config import POSTERS_DIR


def create_poster(city, country, theme, distance):
    """
    Web API compatible wrapper for the upstream create_poster function.
    
    Args:
        city: City name
        country: Country name
        theme: Theme name
        distance: Map radius in meters
    
    Returns:
        Path to the generated poster file
    """
    # Get coordinates using the upstream function
    point = get_coordinates(city, country)
    
    # Generate output filename
    output_file = generate_output_filename(city, theme, path=POSTERS_DIR)
    
    # Call the upstream create_poster with default parameters
    # Using defaults: width=12, height=16, output_format='png'
    upstream_create_poster(
        city=city,
        country=country,
        point=point,
        dist=distance,
        output_file=output_file,
        output_format='png',
        width=12,
        height=16,
        country_label=None,
        name_label=None,
        display_city=None,
        display_country=None,
        fonts=None,
    )
    
    return output_file


# Re-export functions for API compatibility
__all__ = [
    'create_poster',
    'generate_output_filename',
    'get_coordinates',
    'list_themes',
    'get_available_themes',
    'load_theme',
    'POSTERS_DIR',
]
