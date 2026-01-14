# CLI Autocomplete Guide - Using Trie

## Overview

The CLI now has autocomplete functionality powered by the Trie data structure for clinical signs. This allows you to quickly search and autocomplete clinical signs as you type.

## Features

✅ **Trie-based autocomplete** - Fast prefix search using Trie data structure  
✅ **Clinical signs search** - Search for clinical signs by prefix  
✅ **Disease association** - See which diseases are associated with clinical signs  
✅ **Location validation** - Automatic GPS coordinate lookup for cattle hubs  
✅ **Interactive suggestions** - Get real-time suggestions as you type  

## Available Commands

### 1. Search Clinical Signs

Search for clinical signs using Trie prefix matching:

```bash
python -m app.cli search <prefix> [--limit LIMIT]
```

**Examples:**
```bash
# Search for clinical signs starting with "fever"
python -m app.cli search fever

# Search with limit
python -m app.cli search lam --limit 5

# Search for "swelling"
python -m app.cli search swell
```

**Output:**
```
Found 1 clinical sign(s) matching 'fever':

1. fever
   Associated diseases: Bovine Malignant Catarrhal Fever (MCF), Bluetongue Disease (+3 more)
```

### 2. Autocomplete Suggestions

Get autocomplete suggestions for a prefix:

```bash
python -m app.cli autocomplete <prefix>
```

**Examples:**
```bash
python -m app.cli autocomplete fev
python -m app.cli autocomplete lam
python -m app.cli autocomplete dis
```

**Output:**
```
Suggestions for 'fev':
  - fever
```

### 3. Submit Disease Report (Enhanced)

Submit a report with autocomplete support for clinical signs:

```bash
python -m app.cli report <animal_id> <location> <symptoms> [--severity SEVERITY] [--signs SIGNS]
```

**Examples:**
```bash
# Basic report
python -m app.cli report COW001 Ngaoundéré "High fever"

# With clinical signs (comma-separated)
python -m app.cli report COW001 Ngaoundéré "High fever" --signs "fever,nasal discharge"

# With severity level
python -m app.cli report COW001 Maroua "Lameness observed" --severity 3 --signs "lameness"
```

**Features:**
- ✅ Automatic GPS coordinate lookup for known locations
- ✅ Clinical signs validation using Trie
- ✅ Disease association display
- ✅ Location validation

**Output:**
```
Location: Ngaoundéré (7.3277°N, 13.5847°E)
Clinical signs: fever, nasal discharge
✓ Report saved locally

Associated diseases: Bovine Malignant Catarrhal Fever (MCF), ...
```

### 4. List Available Locations

Get all available cattle hub locations:

```bash
python -m app.cli locations
```

**Output:**
```
Available cattle hub locations:

  • Ngaoundéré
    Region: Adamawa
    Coordinates: 7.3277°N, 13.5847°E

  • Maroua
    Region: Far North
    Coordinates: 10.5910°N, 14.3159°E

  • Bamenda
    Region: Northwest
    Coordinates: 5.9597°N, 10.1460°E
```

### 5. Sync Reports

Sync offline reports to the server:

```bash
python -m app.cli sync
```

## How Autocomplete Works

The autocomplete feature uses the **Trie data structure** to provide fast prefix-based search:

1. **Trie Initialization**: On CLI startup, all clinical signs from the dictionary are loaded into a Trie
2. **Prefix Search**: When you type a prefix, the Trie searches for all clinical signs starting with that prefix
3. **Fast Retrieval**: Trie provides O(m) search time where m is the length of the prefix
4. **Disease Association**: Each clinical sign is linked to its associated diseases

## Example Workflow

### Step 1: Search for Clinical Signs
```bash
python -m app.cli search fev
```
This shows all clinical signs starting with "fev" (like "fever")

### Step 2: Get Autocomplete Suggestions
```bash
python -m app.cli autocomplete lam
```
This gives you suggestions for "lam" (like "lameness")

### Step 3: Submit Report with Clinical Signs
```bash
python -m app.cli report COW001 Ngaoundéré "Observed lameness" --signs "lameness,swelling"
```

The CLI will:
- ✅ Validate the location and add GPS coordinates
- ✅ Validate clinical signs using Trie
- ✅ Show associated diseases
- ✅ Save the report locally

## Integration with Trie

The CLI uses the `ClinicalSignsTrie` class from `app.trie_clinical_signs`:

```python
from app.trie_clinical_signs import build_clinical_signs_trie
from app.clinical_signs_dict import CLINICAL_SIGNS_DICT

# Trie is initialized at module level
clinical_signs_trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)

# Autocomplete function uses Trie.search()
def autocomplete_clinical_signs(prefix: str):
    results = clinical_signs_trie.search(prefix)
    return [result['clinical_sign'] for result in results]
```

## Testing the Autocomplete

Run the test script to see autocomplete in action:

```bash
python test_cli_autocomplete.py
```

This will:
1. Show example autocomplete results for common prefixes
2. Provide an interactive mode where you can type prefixes and see suggestions

## Benefits of Trie-Based Autocomplete

1. **Fast Search**: O(m) time complexity for prefix search
2. **Efficient Memory**: Trie structure is memory-efficient
3. **Scalable**: Easy to add new clinical signs
4. **Real-time**: Instant suggestions as you type
5. **Complete**: Finds all matching clinical signs, not just exact matches

## Troubleshooting

**Issue: No suggestions found**
- Check if the prefix is spelled correctly
- Try a shorter prefix (e.g., "fev" instead of "fever")
- Some clinical signs might not exist in the dictionary

**Issue: Command not found**
- Make sure you're in the `Livestock-Disease` directory
- Use: `python -m app.cli` instead of just `app.cli`

**Issue: Import errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that `app.clinical_signs_dict` and `app.trie_clinical_signs` modules exist

## Summary

✅ CLI autocomplete is now connected to Member 1's Trie  
✅ Fast prefix-based search using Trie data structure  
✅ Clinical signs validation and suggestions  
✅ Disease association display  
✅ GPS coordinate integration  

The CLI now provides a powerful command-line interface with intelligent autocomplete powered by the Trie!
