# Livestock Disease Surveillance Network

## Overview
This project implements GPS coordinate tracking for key Cameroonian cattle hubs and a Trie-based dictionary for clinical signs associated with cattle diseases.

## Components

### 1. GPS Coordinates (`gps_coordinates.py`)
Contains GPS coordinates for three key Cameroonian cattle hubs:
- **Ngaoundéré**: 7.3277°N, 13.5847°E (Adamawa Region)
- **Maroua**: 10.5910°N, 14.3159°E (Far North Region)
- **Bamenda**: 5.9597°N, 10.1460°E (Northwest Region)

### 2. Clinical Signs Dictionary (`clinical_signs_dict.py`)
Comprehensive dictionary of clinical signs for various cattle diseases including:
- Bovine Malignant Catarrhal Fever (MCF)
- Fog Fever
- Interdigital Dermatitis
- Bluetongue Disease
- Lumpy Skin Disease
- Milk Fever
- Foot and Mouth Disease
- Bovine Tuberculosis
- Brucellosis
- Anthrax
- Blackleg
- Bovine Respiratory Disease Complex
- Mastitis
- Ketosis
- Grass Tetany

### 3. Clinical Signs Trie (`trie_clinical_signs.py`)
Implements a Trie data structure for efficient storage and retrieval of clinical signs with the following features:
- Insert clinical signs with associated diseases
- Search for clinical signs by prefix
- Check if a clinical sign exists
- Retrieve diseases associated with a clinical sign

## Usage

### Running the main program:
```bash
python main.py
```

### Using GPS coordinates:
```python
from gps_coordinates import get_gps_coordinates, get_all_hubs

# Get coordinates for a specific city
ngaoundere = get_gps_coordinates("Ngaoundéré")
print(ngaoundere)

# Get all hubs
all_hubs = get_all_hubs()
```

### Using the Clinical Signs Trie:
```python
from clinical_signs_dict import CLINICAL_SIGNS_DICT
from trie_clinical_signs import build_clinical_signs_trie

# Build the Trie
trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)

# Search for clinical signs
results = trie.search("fever")
for result in results:
    print(result['clinical_sign'])
    print(result['diseases'])
```

## Files
- `gps_coordinates.py` - GPS coordinates for cattle hubs
- `clinical_signs_dict.py` - Dictionary of clinical signs
- `trie_clinical_signs.py` - Trie implementation for clinical signs
- `main.py` - Main demonstration script
- `README.md` - This file

## References
[13, 14, 15] - As specified in the project requirements
