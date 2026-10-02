import requests


WIKIDATA_URL = "https://query.wikidata.org/sparql"

USER_AGENT = (
    "EducationCareerFinder/0.3 "
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


def fetch_education_records(limit: int = 200) -> list[dict]:
    if limit <= 0:
        raise ValueError("Limit musi być większy od 0.")

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
        {{
            SELECT DISTINCT
                ?person
                ?educationStatement
                ?university
                ?major
            WHERE {{
                ?person wdt:P31 wd:Q5.
                ?person p:P69 ?educationStatement.
                ?educationStatement ps:P69 ?university.
                ?educationStatement pq:P812 ?major.
            }}
            LIMIT {limit}
        }}

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