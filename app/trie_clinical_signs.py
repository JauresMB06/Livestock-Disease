"""
Trie Data Structure for Clinical Signs Dictionary
Livestock Disease Surveillance Network
"""


class TrieNode:
    """Node structure for the Trie data structure."""
    
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.clinical_sign = None
        self.diseases = []  # List of diseases associated with this clinical sign


class ClinicalSignsTrie:
    """Trie data structure for efficient storage and retrieval of clinical signs."""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, clinical_sign, disease=None):
        """
        Insert a clinical sign into the Trie.
        
        Args:
            clinical_sign (str): The clinical sign to insert
            disease (str, optional): Associated disease name
        """
        node = self.root
        clinical_sign = clinical_sign.lower().strip()
        
        for char in clinical_sign:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.clinical_sign = clinical_sign
        
        if disease:
            if disease not in node.diseases:
                node.diseases.append(disease)
    
    def search(self, prefix):
        """
        Search for clinical signs that start with the given prefix.
        
        Args:
            prefix (str): The prefix to search for
        
        Returns:
            list: List of matching clinical signs
        """
        node = self.root
        prefix = prefix.lower().strip()
        
        # Navigate to the node corresponding to the prefix
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all clinical signs from this node
        results = []
        self._collect_words(node, prefix, results)
        return results
    
    def _collect_words(self, node, prefix, results):
        """Helper method to collect all words from a given node."""
        if node.is_end_of_word:
            results.append({
                'clinical_sign': node.clinical_sign,
                'diseases': node.diseases.copy()
            })
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, results)
    
    def contains(self, clinical_sign):
        """
        Check if a clinical sign exists in the Trie.
        
        Args:
            clinical_sign (str): The clinical sign to check
        
        Returns:
            bool: True if the clinical sign exists, False otherwise
        """
        node = self.root
        clinical_sign = clinical_sign.lower().strip()
        
        for char in clinical_sign:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def get_diseases(self, clinical_sign):
        """
        Get all diseases associated with a clinical sign.
        
        Args:
            clinical_sign (str): The clinical sign
        
        Returns:
            list: List of associated diseases
        """
        node = self.root
        clinical_sign = clinical_sign.lower().strip()
        
        for char in clinical_sign:
            if char not in node.children:
                return []
            node = node.children[char]
        
        if node.is_end_of_word:
            return node.diseases.copy()
        return []


def build_clinical_signs_trie(clinical_signs_dict):
    """
    Build a Trie from a dictionary of clinical signs.
    
    Args:
        clinical_signs_dict (dict): Dictionary mapping diseases to their clinical signs
    
    Returns:
        ClinicalSignsTrie: Populated Trie structure
    """
    trie = ClinicalSignsTrie()
    
    for disease, signs in clinical_signs_dict.items():
        for sign in signs:
            trie.insert(sign, disease)
    
    return trie


if __name__ == "__main__":
    # Example usage
    from clinical_signs_dict import CLINICAL_SIGNS_DICT
    
    # Build the Trie
    trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)
    
    # Test search functionality
    print("Testing Clinical Signs Trie\n")
    print("=" * 60)
    
    # Search for clinical signs starting with "fever"
    print("\nSearching for clinical signs starting with 'fever':")
    results = trie.search("fever")
    for result in results[:5]:  # Show first 5 results
        print(f"  - {result['clinical_sign']}")
        if result['diseases']:
            print(f"    Associated diseases: {', '.join(result['diseases'])}")
    
    # Search for clinical signs starting with "lameness"
    print("\nSearching for clinical signs starting with 'lameness':")
    results = trie.search("lameness")
    for result in results:
        print(f"  - {result['clinical_sign']}")
        if result['diseases']:
            print(f"    Associated diseases: {', '.join(result['diseases'])}")
