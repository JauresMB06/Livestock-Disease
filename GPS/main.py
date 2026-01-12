"""
Main module for Livestock Disease Surveillance Network
Combines GPS coordinates and Clinical Signs Trie functionality
"""

from gps_coordinates import get_all_hubs, format_coordinates
from clinical_signs_dict import CLINICAL_SIGNS_DICT, get_all_clinical_signs
from trie_clinical_signs import build_clinical_signs_trie


def main():
    """Main function to demonstrate GPS coordinates and Clinical Signs Trie."""
    
    print("=" * 70)
    print("LIVESTOCK DISEASE SURVEILLANCE NETWORK")
    print("Cameroonian Cattle Hubs - GPS Coordinates & Clinical Signs Dictionary")
    print("=" * 70)
    
    # Display GPS coordinates
    print("\n1. GPS COORDINATES FOR KEY CAMEROONIAN CATTLE HUBS")
    print("-" * 70)
    
    hubs = get_all_hubs()
    for city, data in hubs.items():
        print(f"\n{city}:")
        print(f"  Latitude:  {data['latitude']}°N")
        print(f"  Longitude: {data['longitude']}°E")
        print(f"  Region:    {data['region']}")
        print(f"  Country:   {data['country']}")
    
    # Build and demonstrate Clinical Signs Trie
    print("\n\n2. CLINICAL SIGNS DICTIONARY FOR TRIE")
    print("-" * 70)
    
    print(f"\nTotal diseases in dictionary: {len(CLINICAL_SIGNS_DICT)}")
    print(f"Total unique clinical signs: {len(get_all_clinical_signs())}")
    
    # Build the Trie
    trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)
    print("\n[OK] Clinical Signs Trie built successfully!")
    
    # Demonstrate Trie search functionality
    print("\n\n3. TRIE SEARCH EXAMPLES")
    print("-" * 70)
    
    # Example searches
    search_terms = ["fever", "lameness", "swelling", "discharge", "cough"]
    
    for term in search_terms:
        results = trie.search(term)
        print(f"\nSearching for '{term}':")
        if results:
            print(f"  Found {len(results)} matching clinical sign(s):")
            for result in results[:3]:  # Show first 3 results
                print(f"    - {result['clinical_sign']}")
                if result['diseases']:
                    diseases_str = ', '.join(result['diseases'][:2])
                    if len(result['diseases']) > 2:
                        diseases_str += "..."
                    print(f"      Associated with: {diseases_str}")
        else:
            print(f"  No clinical signs found starting with '{term}'")
    
    print("\n" + "=" * 70)
    print("Setup complete! GPS coordinates and Clinical Signs Trie are ready.")
    print("=" * 70)


if __name__ == "__main__":
    main()
