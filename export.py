import csv
import json
from pathlib import Path

from models import Person


DATA_DIRECTORY = Path("data")


def person_to_dict(person: Person) -> dict:
    educations = []

    for education in person.educations:
        educations.append({
            "university": education.university,
            "major": education.major,
            "degree": education.degree,
            "start_year": education.start_year,
            "end_year": education.end_year,
            "age_at_start": education.age_at_start,
            "status": education.status
        })

    return {
        "name": person.name,
        "wikidata_id": person.wikidata_id,
        "wikidata_url": f"https://www.wikidata.org/wiki/{person.wikidata_id}",
        "birth_year": person.birth_year,
        "number_of_majors": person.get_number_of_majors(),
        "number_of_completed_majors": person.get_number_of_completed_majors(),
        "majors": sorted(person.get_unique_majors()),
        "occupations": sorted(person.occupations),
        "employers": sorted(person.employers),
        "educations": educations
    }


def save_results_to_json(
    people: list[Person],
    filename: str = "results.json"
) -> None:

    DATA_DIRECTORY.mkdir(exist_ok=True)

    data = []

    for person in people:
        data.append(person_to_dict(person))

    path = DATA_DIRECTORY / filename

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def save_results_to_csv(
    people: list[Person],
    filename: str = "results.csv"
) -> None:

    DATA_DIRECTORY.mkdir(exist_ok=True)

    path = DATA_DIRECTORY / filename

    columns = [
        "name",
        "wikidata_id",
        "birth_year",
        "number_of_majors",
        "number_of_completed_majors",
        "majors",
        "occupations",
        "employers",
        "wikidata_url"
    ]

    with open(
        path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns,
            delimiter=";"
        )

        writer.writeheader()

        for person in people:
            writer.writerow({
                "name": person.name,
                "wikidata_id": person.wikidata_id,
                "birth_year": person.birth_year,
                "number_of_majors": person.get_number_of_majors(),
                "number_of_completed_majors":
                    person.get_number_of_completed_majors(),
                "majors": " | ".join(
                    sorted(person.get_unique_majors())
                ),
                "occupations": " | ".join(
                    sorted(person.occupations)
                ),
                "employers": " | ".join(
                    sorted(person.employers)
                ),
                "wikidata_url":
                    f"https://www.wikidata.org/wiki/{person.wikidata_id}"
            })