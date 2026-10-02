from analysis import build_people, filter_people_with_min_majors
from wikidata import fetch_person_ids, fetch_education_for_people


MIN_MAJORS = 2

BATCH_SIZE = 50
MAX_BATCHES = 10

TARGET_RESULTS = 10


def format_value(value: str | int | None) -> str:
    if value is None:
        return "brak danych"

    return str(value)


def main() -> None:
    print("Education Career Finder")
    print("-----------------------")

    found_people = {}
    checked_people = 0

    try:
        for batch_number in range(MAX_BATCHES):
            offset = batch_number * BATCH_SIZE

            person_ids = fetch_person_ids(
                limit=BATCH_SIZE,
                offset=offset
            )

            if not person_ids:
                break

            checked_people += len(person_ids)

            records = fetch_education_for_people(person_ids)
            people = build_people(records)

            candidates = filter_people_with_min_majors(
                people,
                MIN_MAJORS
            )

            for person in candidates:
                found_people[person.wikidata_id] = person

            print(
                f"Sprawdzono: {checked_people} osób | "
                f"znaleziono: {len(found_people)}"
            )

            if len(found_people) >= TARGET_RESULTS:
                break

    except (RuntimeError, ValueError) as error:
        print()
        print("Błąd:")
        print(error)
        return

    results = list(found_people.values())

    results.sort(
        key=lambda person: person.get_number_of_majors(),
        reverse=True
    )

    if not results:
        print()
        print("Nie znaleziono osób spełniających kryteria.")
        return

    print()
    print("Wyniki")
    print("------")

    for person in results[:TARGET_RESULTS]:
        print()
        print(
            person.name,
            f"({person.wikidata_id})",
            "-",
            person.get_number_of_majors(),
            "różne kierunki"
        )

        print(
            "Kierunki:",
            ", ".join(sorted(person.get_unique_majors()))
        )

        for education in person.educations:
            print(
                " -",
                format_value(education.major),
                "| uczelnia:",
                format_value(education.university),
                "| stopień:",
                format_value(education.degree),
                "| lata:",
                format_value(education.start_year),
                "-",
                format_value(education.end_year),
                "| wiek:",
                format_value(education.age_at_start),
                "| status:",
                education.status
            )


if __name__ == "__main__":
    main()