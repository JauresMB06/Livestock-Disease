
import typer
from typing import List, Optional
from app.services.sync_service import save_local_report, sync_reports
from app.clinical_signs_dict import CLINICAL_SIGNS_DICT
from app.trie_clinical_signs import build_clinical_signs_trie
from app.gps_coordinates import get_all_hubs, get_gps_coordinates

# Initialize Trie for autocomplete
clinical_signs_trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)

app = typer.Typer()

def autocomplete_clinical_signs(ctx: typer.Context, incomplete: str) -> List[str]:
    """
    Autocomplete function for clinical signs using Trie.
    This provides shell completion suggestions.
    """
    if not incomplete:
        # Return all clinical signs if no prefix
        results = clinical_signs_trie.search("")
    else:
        # Search Trie for matching clinical signs
        results = clinical_signs_trie.search(incomplete)
    
    # Return just the clinical sign strings for autocomplete
    return [result['clinical_sign'] for result in results[:20]]  # Limit to 20 suggestions

def get_location_suggestions() -> List[str]:
    """Get list of available cattle hub locations."""
    hubs = get_all_hubs()
    return list(hubs.keys())

@app.command()
def report(
    animal_id: str = typer.Argument(..., help="Animal ID"),
    location: str = typer.Argument(..., help="Location (Ngaoundéré, Maroua, or Bamenda)"),
    symptoms: str = typer.Argument(..., help="Symptoms description"),
    severity: int = typer.Option(1, "--severity", "-s", help="Severity level (1-5)"),
    clinical_signs: Optional[str] = typer.Option(None, "--signs", "-c", help="Clinical signs (comma-separated)")
):
    """
    Submit a disease report with autocomplete support.
    
    Examples:
        python -m app.cli report COW001 Ngaoundéré "High fever" --signs "fever,nasal discharge"
    """
    # Validate location
    hub_coords = get_gps_coordinates(location)
    if not hub_coords:
        typer.echo(f"Warning: '{location}' not found in cattle hubs. Using provided location.")
        latitude, longitude = None, None
    else:
        latitude = hub_coords["latitude"]
        longitude = hub_coords["longitude"]
        typer.echo(f"Location: {location} ({latitude}°N, {longitude}°E)")
    
    # Parse clinical signs if provided
    clinical_signs_list = []
    if clinical_signs:
        clinical_signs_list = [s.strip() for s in clinical_signs.split(",")]
        typer.echo(f"Clinical signs: {', '.join(clinical_signs_list)}")
    
    report_data = {
        "animal_id": animal_id,
        "location": location,
        "symptoms": symptoms,
        "severity": severity,
        "latitude": latitude,
        "longitude": longitude,
        "clinical_signs": clinical_signs_list if clinical_signs_list else None
    }
    
    save_local_report(report_data)
    typer.echo("[OK] Report saved locally")
    
    # Show associated diseases if clinical signs provided
    if clinical_signs_list:
        all_diseases = set()
        for sign in clinical_signs_list:
            diseases = clinical_signs_trie.get_diseases(sign)
            all_diseases.update(diseases)
        
        if all_diseases:
            typer.echo(f"\nAssociated diseases: {', '.join(list(all_diseases)[:5])}")

@app.command()
def sync():
    """Sync offline reports to the server."""
    synced = sync_reports()
    typer.echo(f"[OK] {synced} reports synced")

@app.command()
def search(
    prefix: str = typer.Argument(..., help="Prefix to search for clinical signs"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results")
):
    """
    Search for clinical signs using Trie autocomplete.
    
    Examples:
        python -m app.cli search fever
        python -m app.cli search lame --limit 5
    """
    results = clinical_signs_trie.search(prefix)
    
    if not results:
        typer.echo(f"No clinical signs found starting with '{prefix}'")
        return
    
    typer.echo(f"\nFound {len(results)} clinical sign(s) matching '{prefix}':\n")
    
    for i, result in enumerate(results[:limit], 1):
        typer.echo(f"{i}. {result['clinical_sign']}")
        if result['diseases']:
            diseases_str = ', '.join(result['diseases'][:3])
            if len(result['diseases']) > 3:
                diseases_str += f" (+{len(result['diseases']) - 3} more)"
            typer.echo(f"   Associated diseases: {diseases_str}")
        typer.echo()

@app.command()
def autocomplete(
    prefix: str = typer.Argument(..., help="Prefix for autocomplete suggestions")
):
    """
    Get autocomplete suggestions for clinical signs.
    Useful for interactive CLI or shell completion.
    
    Examples:
        python -m app.cli autocomplete fev
    """
    suggestions = autocomplete_clinical_signs(None, prefix)
    
    if not suggestions:
        typer.echo(f"No suggestions for '{prefix}'")
        return
    
    typer.echo(f"Suggestions for '{prefix}':")
    for suggestion in suggestions:
        typer.echo(f"  - {suggestion}")

@app.command()
def locations():
    """List all available cattle hub locations."""
    hubs = get_all_hubs()
    typer.echo("\nAvailable cattle hub locations:\n")
    for city, data in hubs.items():
        typer.echo(f"  • {city}")
        typer.echo(f"    Region: {data['region']}")
        typer.echo(f"    Coordinates: {data['latitude']}°N, {data['longitude']}°E\n")

if __name__ == "__main__":
    app()
