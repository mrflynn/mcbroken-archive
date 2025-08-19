# A content script for use with git-history to flatten the content of the
# mcbroken.json file so that it is row-native instead of a nested JSON
# structure.


def get_coordinates(data):
    coordinates = data.get("geometry", {}).get("coordinates", [])

    return {
        "latitude": float(next(itertools.islice(coordinates, 1, 2), 0.0)),
        "longitude": float(next(itertools.islice(coordinates, 0, 1), 0.0)),
    }


def get_last_checked(data):
    last_checked = re.search(
        r"\b(\d+)\b", data.get("properties", {}).get("last_checked", "")
    )

    if last_checked:
        return int(last_checked.group(0))

    return 0


for entry in json.loads(content):
    properties_to_keep = set(entry.get("properties", {}).keys()).difference(
        ["last_checked"]
    )

    yield {
        # Extract coordinates from GeoJSON list.
        **get_coordinates(entry),
        # Keep all properties except "last_checked" which will be processed
        # more later.
        **dict(
            zip(
                properties_to_keep,
                operator.itemgetter(*properties_to_keep)(entry.get("properties", {})),
            )
        ),
        # Extract numeric minute value from properties.last_checked.
        "last_checked_minutes": get_last_checked(entry),
    }
