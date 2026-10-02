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
        ?person wdt:P31 wd:Q5.
        ?person p:P69 ?educationStatement.
        ?educationStatement ps:P69 ?university.
        ?educationStatement pq:P812 ?major.

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
    LIMIT 10
    """

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

    data = response.json()

    return data["results"]["bindings"]