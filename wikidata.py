import requests


WIKIDATA_URL = "https://query.wikidata.org/sparql"

USER_AGENT = (
    "EducationCareerFinder/0.4 "
    "(https://github.com/Kitekso/education_career_finder)"
)


def run_query(query: str) -> list[dict]:
    try:
        response = requests.get(
            WIKIDATA_URL,
            params={
                "query": query,
                "format": "json"
            },
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=45
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "Wikidata nie odpowiedziała wystarczająco szybko."
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Błąd połączenia z Wikidata: {error}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            "Nie udało się odczytać odpowiedzi Wikidata jako JSON."
        ) from error

    return data.get("results", {}).get("bindings", [])


def get_wikidata_id(entity_url: str) -> str:
    return entity_url.rsplit("/", 1)[-1]


def fetch_person_ids(limit: int = 50, offset: int = 0) -> list[str]:
    query = f"""
    SELECT DISTINCT ?person
    WHERE {{
        ?person wdt:P31 wd:Q5.
        ?person p:P69 ?educationStatement.
        ?educationStatement pq:P812 ?major.
    }}
    LIMIT {limit}
    OFFSET {offset}
    """

    records = run_query(query)
    person_ids = []

    for record in records:
        person = record.get("person")

        if person is None:
            continue

        person_ids.append(
            get_wikidata_id(person["value"])
        )

    return person_ids


def fetch_education_for_people(person_ids: list[str]) -> list[dict]:
    if not person_ids:
        return []

    valid_ids = []

    for person_id in person_ids:
        if person_id.startswith("Q") and person_id[1:].isdigit():
            valid_ids.append(person_id)

    if not valid_ids:
        return []

    values = " ".join(
        f"wd:{person_id}"
        for person_id in valid_ids
    )

    query = f"""
    SELECT DISTINCT
        ?person
        ?personLabel
        ?birthDate
        ?university
        ?universityLabel
        ?major
        ?majorLabel
        ?degree
        ?degreeLabel
        ?startDate
        ?endDate
    WHERE {{
        VALUES ?person {{
            {values}
        }}

        ?person p:P69 ?educationStatement.
        ?educationStatement ps:P69 ?university.
        ?educationStatement pq:P812 ?major.

        OPTIONAL {{
            ?educationStatement pq:P512 ?degree.
        }}

        OPTIONAL {{
            ?educationStatement pq:P580 ?startDate.
        }}

        OPTIONAL {{
            ?educationStatement pq:P582 ?endDate.
        }}

        OPTIONAL {{
            ?person wdt:P569 ?birthDate.
        }}

        SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "pl,en".
        }}
    }}
    """

    return run_query(query)