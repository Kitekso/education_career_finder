from models import Education, Person
from wikidata import fetch_education_records


def main():
    records = fetch_education_records()

    print("Liczba rekordów:", len(records))

    for record in records:
        person_name = record["personLabel"]["value"]
        major_name = record["majorLabel"]["value"]
        university_name = record["universityLabel"]["value"]

        print(
            person_name,
            "|",
            major_name,
            "|",
            university_name
        )


if __name__ == "__main__":
    main()
