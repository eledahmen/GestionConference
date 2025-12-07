import os
import django
from fastmcp import FastMCP
from asgiref.sync import sync_to_async

# -----------------------------------------------------------
# Initialisation de Django
# -----------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference.settings")
django.setup()

# Import des modèles (après django.setup())
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Création du serveur MCP
mcp = FastMCP("Conference Assistant")

# -----------------------------------------------------------
# 1. TOOL : Liste des conférences
# -----------------------------------------------------------
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""

    @sync_to_async
    def _get_conferences():
        return list(Conference.objects.all())

    conferences = await _get_conferences()

    if not conferences:
        return "No conferences found."

    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

# -----------------------------------------------------------
# 2. TOOL : Détails d'une conférence
# -----------------------------------------------------------
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""

    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    conference = await _get_conference()

    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conference:
        return f"Conference '{name}' not found."

    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# -----------------------------------------------------------
# 3. TOOL : Sessions d'une conférence
# -----------------------------------------------------------
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""

    @sync_to_async
    def _get_sessions():
        try:
            conf = Conference.objects.get(name__icontains=conference_name)
            return list(conf.sessions.all()), conf
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    sessions, conf = await _get_sessions()

    if sessions == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."

    if conf is None:
        return f"Conference '{conference_name}' not found."

    if not sessions:
        return f"No sessions found for conference '{conf.name}'."

    return "\n".join([
        f"- {s.title} ({s.start_time} - {s.end_time}) | Room: {s.room}\n  Topic: {s.topic}"
        for s in sessions
    ])

# -----------------------------------------------------------
# 4. TOOL BONUS : Filtrer les conférences par thème
# -----------------------------------------------------------
@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filter conferences by theme."""

    @sync_to_async
    def _filter():
        return list(Conference.objects.filter(theme__icontains=theme))

    conferences = await _filter()

    if not conferences:
        return f"No conferences found for theme '{theme}'."

    return "\n".join([f"- {c.name} ({c.location})" for c in conferences])

# -----------------------------------------------------------
# Lancement du serveur MCP
# -----------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
