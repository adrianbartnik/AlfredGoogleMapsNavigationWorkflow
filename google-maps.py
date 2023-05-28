import json
import os
import sys
from enum import Enum
import urllib.parse
import re


class TravelMode(Enum):
    DRIVING = "driving"
    WALKING = "walking"
    BICYCLING = "bicycling"
    TRANSIT = "transit"
    BEST = "best"


HOME_ADDRESS = os.environ.get("home_address")
WORK_ADDRESS = os.environ.get("work_address")
TRAVEL_MODE = TravelMode(os.environ.get("travel_mode"))
LOCALISATION = os.environ.get("localisation")

BASE_URL = f"https://www.google{LOCALISATION}/maps/dir/?api=1&"

DRIVING_TRAVEL_MODE_SYNONYMS = ["car", "drive", "driving"]
BIKING_TRAVEL_MODE_SYNONYMS = ["bike", "cycle", "bicycling"]
TRANSIT_TRAVEL_MODE_SYNONYMS = ["public", "transit", "train"]
WALKING_TRAVEL_MODE_SYNONYMS = ["walk", "walking"]
BEST_TRAVEL_MODE_SYNONYMS = ["default", "best", "adaptive"]
ALL_TRAVEL_MODES = (
    DRIVING_TRAVEL_MODE_SYNONYMS
    + BIKING_TRAVEL_MODE_SYNONYMS
    + TRANSIT_TRAVEL_MODE_SYNONYMS
    + WALKING_TRAVEL_MODE_SYNONYMS
    + BEST_TRAVEL_MODE_SYNONYMS
)


def _parse_travel_mode(travel_mode_str: str) -> TravelMode:
    if travel_mode_str in DRIVING_TRAVEL_MODE_SYNONYMS:
        return TravelMode.DRIVING
    if travel_mode_str in BIKING_TRAVEL_MODE_SYNONYMS:
        return TravelMode.BICYCLING
    if travel_mode_str in TRANSIT_TRAVEL_MODE_SYNONYMS:
        return TravelMode.TRANSIT
    if travel_mode_str in WALKING_TRAVEL_MODE_SYNONYMS:
        return TravelMode.WALKING
    if travel_mode_str in BEST_TRAVEL_MODE_SYNONYMS:
        return TravelMode.BEST
    else:
        return TRAVEL_MODE


def prepare_google_maps_url(
    origin: str = "", destination: str = "", travel_mode: TravelMode = TRAVEL_MODE
):
    return (
        BASE_URL + f"origin={urllib.parse.quote(origin)}"
        f"&destination={urllib.parse.quote(destination)}"
        f"&travelmode={urllib.parse.quote(travel_mode.value)}"
    )


def prepare_from_query(query: str):
    pattern = f"^(from|to) (work|home) (.+?)(?: +({'|'.join(ALL_TRAVEL_MODES)}))?$"

    match = re.search(pattern, query)

    if match:
        operation = match.group(1)
        work_or_home = match.group(2)
        destination = match.group(3)
        travel_mode = _parse_travel_mode(match.group(4))

        origin = HOME_ADDRESS if work_or_home == "home" else WORK_ADDRESS

        if not origin:
            return f"ERROR: Your {'home' if work_or_home == 'home' else 'work'} address is not set. You can do this in the Workflow Configuration."

        if operation == "to":
            origin, destination = destination, origin

        return prepare_google_maps_url(
            origin=origin, destination=destination, travel_mode=travel_mode
        )
    else:
        return query


def prepare_from_default_query(query: str) -> str:
    query_split = query.rsplit(" ", 1)

    if len(query_split) == 2 and query_split[1] in ALL_TRAVEL_MODES:
        travel_mode = _parse_travel_mode(query_split[1])

        return prepare_google_maps_url(
            destination=query_split[0], travel_mode=travel_mode
        )
    else:
        return prepare_google_maps_url(destination=query)


if __name__ == "__main__":
    search_query = sys.argv[1].lower()

    print(
        "Starting Mappy for:", search_query, WORK_ADDRESS, HOME_ADDRESS, file=sys.stderr
    )

    items = []

    if not search_query.startswith("from ") and not search_query.startswith("to "):
        items.append(
            {
                "title": "<address>",
                "subtitle": "Navigate to address based on current location. Optional: append <travelmode>",
                "arg": prepare_from_default_query(search_query),
                "icon": {"path": "assets/icon.png"},
            }
        )

    if (
        search_query.startswith(tuple(["f", "fr", "fro", "from"]))
        or len(search_query) == 0
    ):
        items.append(
            {
                "title": "From <home|work> <address>",
                "subtitle": "Navigate to <address> from home or work address. Optional: append <travelmode>",
                "arg": prepare_from_query(query=search_query),
                "icon": {"path": "assets/icon.png"},
            }
        )

    if search_query.startswith(tuple(["t", "to"])) or len(search_query) == 0:
        items.append(
            {
                "title": "To <home|work> <address>",
                "subtitle": "Navigate home or work to <address>. Optional: append <travelmode>",
                "arg": prepare_from_query(query=search_query),
                "icon": {"path": "assets/icon.png"},
            }
        )

    sys.stdout.write(json.dumps({"items": items}))
