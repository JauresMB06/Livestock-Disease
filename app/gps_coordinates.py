"""
GPS Coordinates for Key Cameroonian Cattle Hubs
Livestock Disease Surveillance Network
"""

# GPS coordinates for key Cameroonian cattle hubs
CATTLE_HUBS = {
    "Ngaoundéré": {
        "latitude": 7.3277,
        "longitude": 13.5847,
        "city": "Ngaoundéré",
        "region": "Adamawa",
        "country": "Cameroon"
    },
    "Maroua": {
        "latitude": 10.5910,
        "longitude": 14.3159,
        "city": "Maroua",
        "region": "Far North",
        "country": "Cameroon"
    },
    "Bamenda": {
        "latitude": 5.9597,
        "longitude": 10.1460,
        "city": "Bamenda",
        "region": "Northwest",
        "country": "Cameroon"
    }
}


def get_gps_coordinates(city_name):
    """
    Retrieve GPS coordinates for a given cattle hub city.
    
    Args:
        city_name (str): Name of the city (Ngaoundéré, Maroua, or Bamenda)
    
    Returns:
        dict: Dictionary containing latitude, longitude, and city information
        None: If city not found
    """
    return CATTLE_HUBS.get(city_name.title())


def get_all_hubs():
    """
    Get all cattle hub GPS coordinates.
    
    Returns:
        dict: Dictionary of all cattle hubs with their GPS coordinates
    """
    return CATTLE_HUBS.copy()


def format_coordinates(city_name):
    """
    Format GPS coordinates as a readable string.
    
    Args:
        city_name (str): Name of the city
    
    Returns:
        str: Formatted coordinate string
    """
    hub = get_gps_coordinates(city_name)
    if hub:
        return f"{hub['city']}: {hub['latitude']}°N, {hub['longitude']}°E"
    return None


if __name__ == "__main__":
    # Display all GPS coordinates
    print("GPS Coordinates for Key Cameroonian Cattle Hubs\n")
    print("=" * 60)
    
    for city, data in CATTLE_HUBS.items():
        print(f"\n{city}:")
        print(f"  Latitude:  {data['latitude']}°N")
        print(f"  Longitude: {data['longitude']}°E")
        print(f"  Region:    {data['region']}")
        print(f"  Country:   {data['country']}")
