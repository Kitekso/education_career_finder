from analysis import build_people
from models import Education, Person
from wikidata import (
    fetch_education_records,
    fetch_people_with_multiple_majors
)

candidates = fetch_people_with_multiple_majors()

print("Kandydaci:")

for candidate in candidates:
    print(
        candidate["person"]["value"],
        "- liczba kierunków:",
        candidate["majorCount"]["value"]
    )

def main():

    try:
        records = fetch_education_records()

    except RuntimeError as error:
        print("Błąd pobierania danych:")
        print(error)
        return
    
    people = build_people(records)

    print("Liczba rekordów:", len(records))
    print("Liczba osób:", len(people))

    for person in people.values():
        print()
        print(person.name, "-", person.wikidata_id)

        print("Kierunki:", person.get_unique_majors())

        for education in person.educations:
            print(
                "  ",
                education.major,
                "|",
                education.university,
                "|",
                education.start_year,
                "-",
                education.end_year
            )


if __name__ == "__main__":
    main()
