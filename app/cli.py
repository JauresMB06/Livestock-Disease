
import typer
from services.sync_service import save_local_report, sync_reports

app = typer.Typer()

@app.command()
def report(animal_id: str, location: str, symptoms: str, severity: int = 1):
    report_data = {
        "animal_id": animal_id,
        "location": location,
        "symptoms": symptoms,
        "severity": severity
    }
    save_local_report(report_data)
    typer.echo("Report saved locally")

@app.command()
def sync():
    synced = sync_reports()
    typer.echo(f"{synced} reports synced")

if __name__ == "__main__":
    app()
