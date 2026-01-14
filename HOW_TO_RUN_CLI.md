# How to Run CLI Commands in Terminal

## Step-by-Step Instructions

### Step 1: Open Terminal

**Windows:**
- Press `Windows Key + R`
- Type `cmd` and press Enter
- OR press `Windows Key + X` and select "Terminal" or "PowerShell"

**Git Bash (if installed):**
- Right-click in the folder → "Git Bash Here"

### Step 2: Navigate to Project Directory

Type this command and press Enter:

```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
```

**Verify you're in the right place:**
```bash
dir
```
You should see folders like `app`, `venv`, and files like `requirements.txt`

### Step 3: Run CLI Commands

## Available Commands

### 1. Search Clinical Signs

**Command:**
```bash
python -m app.cli search fever
```

**More examples:**
```bash
python -m app.cli search lam
python -m app.cli search swell --limit 5
python -m app.cli search dis
```

**What it does:** Searches for clinical signs starting with the prefix using Trie

---

### 2. Get Autocomplete Suggestions

**Command:**
```bash
python -m app.cli autocomplete fev
```

**More examples:**
```bash
python -m app.cli autocomplete lam
python -m app.cli autocomplete cou
```

**What it does:** Returns autocomplete suggestions for the prefix

---

### 3. Submit Disease Report

**Basic command:**
```bash
python -m app.cli report COW001 Ngaoundéré "High fever"
```

**With clinical signs:**
```bash
python -m app.cli report COW001 Ngaoundéré "High fever" --signs "fever,nasal discharge"
```

**With severity level:**
```bash
python -m app.cli report COW001 Maroua "Lameness observed" --severity 3 --signs "lameness"
```

**What it does:** 
- Validates location and adds GPS coordinates
- Validates clinical signs using Trie
- Shows associated diseases
- Saves report locally

---

### 4. List Available Locations

**Command:**
```bash
python -m app.cli locations
```

**What it does:** Shows all cattle hub locations with GPS coordinates

---

### 5. Sync Reports

**Command:**
```bash
python -m app.cli sync
```

**What it does:** Syncs offline reports to the server

---

### 6. Get Help

**See all commands:**
```bash
python -m app.cli --help
```

**Get help for specific command:**
```bash
python -m app.cli report --help
python -m app.cli search --help
```

---

## Quick Reference

### Full Command Format:
```bash
python -m app.cli <command> <arguments> [options]
```

### Common Patterns:

**Search:**
```bash
python -m app.cli search <prefix> [--limit NUMBER]
```

**Autocomplete:**
```bash
python -m app.cli autocomplete <prefix>
```

**Report:**
```bash
python -m app.cli report <animal_id> <location> <symptoms> [--severity NUMBER] [--signs "sign1,sign2"]
```

**Locations:**
```bash
python -m app.cli locations
```

---

## Example Session

Here's a complete example of using the CLI:

```bash
# 1. Navigate to project
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease

# 2. Search for clinical signs
python -m app.cli search fever

# 3. Get autocomplete suggestions
python -m app.cli autocomplete lam

# 4. List locations
python -m app.cli locations

# 5. Submit a report
python -m app.cli report COW001 Ngaoundéré "High fever observed" --signs "fever,nasal discharge" --severity 3

# 6. Sync reports
python -m app.cli sync
```

---

## Troubleshooting

### Issue: "python is not recognized"
**Solution:** Try using `py` instead:
```bash
py -m app.cli search fever
```

### Issue: "No module named 'app'"
**Solution:** Make sure you're in the `Livestock-Disease` directory:
```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
dir  # Should see 'app' folder
```

### Issue: "No module named 'typer'"
**Solution:** Install dependencies:
```bash
pip install typer
```

### Issue: Command not working
**Solution:** Check you're using the correct format:
```bash
python -m app.cli <command>
```
NOT: `app.cli <command>` or `python app/cli.py <command>`

---

## Tips

1. **Always use:** `python -m app.cli` (not just `app.cli`)
2. **Use quotes** for multi-word arguments: `"High fever"`
3. **Use commas** for multiple clinical signs: `"fever,nasal discharge"`
4. **Check help** if unsure: `python -m app.cli --help`

---

## Copy-Paste Ready Commands

Copy these directly into your terminal:

```bash
# Navigate to project
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease

# Search for "fever"
python -m app.cli search fever

# Get autocomplete for "lam"
python -m app.cli autocomplete lam

# List locations
python -m app.cli locations

# Submit report
python -m app.cli report COW001 Ngaoundéré "High fever" --signs "fever"
```

---

That's it! You're ready to use the CLI with Trie autocomplete! 🚀
