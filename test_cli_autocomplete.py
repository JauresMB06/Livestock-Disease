"""
Test script to demonstrate CLI autocomplete with Trie
"""

from app.clinical_signs_dict import CLINICAL_SIGNS_DICT
from app.trie_clinical_signs import build_clinical_signs_trie

# Initialize Trie
trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)

def autocomplete_clinical_signs(prefix: str, limit: int = 10):
    """Get autocomplete suggestions from Trie."""
    results = trie.search(prefix)
    return [result['clinical_sign'] for result in results[:limit]]

def interactive_autocomplete():
    """Interactive autocomplete demo."""
    print("=" * 70)
    print("CLI AUTCOMPLETE DEMONSTRATION - Using Trie")
    print("=" * 70)
    print("\nType a prefix to see autocomplete suggestions.")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            prefix = input("Enter prefix: ").strip()
            
            if prefix.lower() == 'exit':
                break
            
            if not prefix:
                print("Please enter a prefix.\n")
                continue
            
            suggestions = autocomplete_clinical_signs(prefix, limit=10)
            
            if suggestions:
                print(f"\nFound {len(suggestions)} suggestion(s) for '{prefix}':")
                for i, suggestion in enumerate(suggestions, 1):
                    # Get diseases for this sign
                    diseases = trie.get_diseases(suggestion)
                    diseases_str = ', '.join(diseases[:2]) if diseases else "No diseases"
                    if len(diseases) > 2:
                        diseases_str += f" (+{len(diseases) - 2} more)"
                    print(f"  {i}. {suggestion}")
                    print(f"     → {diseases_str}")
                print()
            else:
                print(f"No suggestions found for '{prefix}'\n")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}\n")

def demo_examples():
    """Demonstrate autocomplete with example prefixes."""
    print("=" * 70)
    print("AUTOCOMPLETE EXAMPLES")
    print("=" * 70)
    
    examples = ["fev", "lam", "swell", "dis", "cou", "nas"]
    
    for prefix in examples:
        suggestions = autocomplete_clinical_signs(prefix, limit=5)
        print(f"\nPrefix: '{prefix}'")
        if suggestions:
            print(f"  Found {len(suggestions)} suggestion(s):")
            for suggestion in suggestions:
                print(f"    - {suggestion}")
        else:
            print("  No suggestions found")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    # Run examples
    demo_examples()
    
    # Run interactive demo
    print("\n")
    interactive_autocomplete()
