# Livestock Disease Surveillance Network

A comprehensive system for monitoring and reporting livestock diseases in Cameroon, combining GPS coordinate tracking for cattle hubs and a Trie-based clinical signs dictionary.

## Features

### 1. GPS Coordinates for Cameroonian Cattle Hubs
- **Ngaoundéré**: 7.3277°N, 13.5847°E (Adamawa Region)
- **Maroua**: 10.5910°N, 14.3159°E (Far North Region)
- **Bamenda**: 5.9597°N, 10.1460°E (Northwest Region)

### 2. Clinical Signs Dictionary & Trie
- 15 different cattle diseases
- 124 unique clinical signs
- Fast prefix-based search using Trie data structure
- Disease association mapping

### 3. FastAPI Backend
- RESTful API for disease reporting
- Offline storage with SQLite
- Automatic GPS coordinate lookup
- Clinical signs to disease mapping

## Project Structure

```
Livestock-Disease/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── database/
│   │   └── local_db.py         # SQLite database operations
│   ├── schemas/
│   │   └── report.py           # Pydantic models
│   ├── services/
│   │   └── sync_service.py     # Sync service for offline reports
│   ├── gps_coordinates.py      # GPS coordinates for cattle hubs
│   ├── clinical_signs_dict.py  # Clinical signs dictionary
│   ├── trie_clinical_signs.py  # Trie implementation
│   ├── main.py                 # FastAPI application
│   └── cli.py                  # CLI tool
├── offline_reports.db          # SQLite database
├── requirements.txt            # Python dependencies
└── run_demo.py                 # Demo script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JauresMB06/Livestock-Disease.git
cd Livestock-Disease
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the API Server

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Alternative docs: http://127.0.0.1:8000/redoc

### Running the Demo

Run the integrated demo:
```bash
python run_demo.py
```

### Using the CLI

Report a disease outbreak:
```bash
python -m app.cli report "COW001" "Ngaoundéré" "High fever, nasal discharge" 3
```

Sync offline reports:
```bash
python -m app.cli sync
```

## API Endpoints

### Disease Reports
- `POST /api/report` - Submit a disease report
  ```json
  {
    "animal_id": "COW001",
    "location": "Ngaoundéré",
    "symptoms": "High fever, nasal discharge",
    "severity": 3,
    "clinical_signs": ["fever", "nasal discharge"]
  }
  ```

### GPS Coordinates
- `GET /api/gps/hubs` - Get all cattle hub coordinates
- `GET /api/gps/hubs/{city_name}` - Get coordinates for a specific hub

### Clinical Signs
- `GET /api/clinical-signs` - Get all clinical signs
- `GET /api/clinical-signs/search?prefix={prefix}` - Search clinical signs by prefix
- `GET /api/clinical-signs/diseases?sign={sign}` - Get diseases for a clinical sign
- `GET /api/clinical-signs/dictionary` - Get complete dictionary

## Example API Usage

### Get GPS coordinates for all hubs:
```bash
curl http://127.0.0.1:8000/api/gps/hubs
```

### Search clinical signs:
```bash
curl "http://127.0.0.1:8000/api/clinical-signs/search?prefix=fever"
```

### Submit a report:
```bash
curl -X POST http://127.0.0.1:8000/api/report \
  -H "Content-Type: application/json" \
  -d '{
    "animal_id": "COW001",
    "location": "Ngaoundéré",
    "symptoms": "High fever",
    "severity": 3,
    "clinical_signs": ["fever"]
  }'
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `typer` - CLI framework
- `requests` - HTTP library
- `pydantic` - Data validation

## Development

### Testing the Integration

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Run the demo:
```bash
python run_demo.py
```

3. Visit the interactive docs:
```
http://127.0.0.1:8000/docs
```

## Team Contributions

- GPS Coordinates & Clinical Signs Dictionary: Integrated from GPS module
- FastAPI Backend: Team members' contribution
- Database & Sync Service: Team members' contribution

## References

[13, 14, 15] - As specified in project requirements
