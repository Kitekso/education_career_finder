import requests


WIKIDATA_URL = "https://query.wikidata.org/sparql"


def fetch_education_records() -> list[dict]:
    query = """
    SELECT
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
    WHERE {

        {
            SELECT
                ?person
                ?educationStatement
                ?university
                ?major
            WHERE {
                ?person wdt:P31 wd:Q5.
                ?person p:P69 ?educationStatement.

                ?educationStatement ps:P69 ?university.
                ?educationStatement pq:P812 ?major.
            }
            LIMIT 20
        }

        OPTIONAL {
            ?educationStatement pq:P512 ?degree.
        }

        OPTIONAL {
            ?educationStatement pq:P580 ?startDate.
        }

        OPTIONAL {
            ?educationStatement pq:P582 ?endDate.
        }

        OPTIONAL {
            ?person wdt:P569 ?birthDate.
        }

        SERVICE wikibase:label {
            bd:serviceParam wikibase:language "pl,en".
        }
    }
    """

    try:
        response = requests.get(
            WIKIDATA_URL,
            params={
                "query": query,
                "format": "json"
            },
            headers={
                "User-Agent": "EducationCareerFinder/0.2"
            },
            timeout=30
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "Wikidata nie odpowiedziała w ciągu 30 sekund."
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Błąd połączenia z Wikidata: {error}"
        ) from error

    data = response.json()

    return data["results"]["bindings"]