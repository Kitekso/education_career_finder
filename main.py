from analysis import build_people, filter_people_with_min_majors
from wikidata import fetch_education_records


SAMPLE_LIMIT = 200
MIN_MAJORS = 2


def format_value(value: str | int | None) -> str:
    if value is None:
        return "brak danych"

    return str(value)


def main() -> None:
    print("Education Career Finder")
    print("-----------------------")

    try:
        records = fetch_education_records(limit=SAMPLE_LIMIT)

    except (RuntimeError, ValueError) as error:
        print("Błąd:")
        print(error)
        return

    people = build_people(records)
    candidates = filter_people_with_min_majors(people, MIN_MAJORS)

    print()
    print("Pobrane rekordy:", len(records))
    print("Unikalne osoby:", len(people))
    print(
        f"Osoby z co najmniej {MIN_MAJORS} różnymi kierunkami:",
        len(candidates)
    )

    if not candidates:
        print()
        print("W tej próbce nie znaleziono osób z wieloma kierunkami.")
        return

    for person in candidates:
        print()
        print(
            person.name,
            f"({person.wikidata_id})",
            "-",
            person.get_number_of_majors(),
            "kierunki"
        )

        print(
            "Kierunki:",
            ", ".join(sorted(person.get_unique_majors()))
        )

        for education in person.educations:
            print(
                " -",
                format_value(education.major),
                "|",
                format_value(education.university),
                "|",
                format_value(education.degree),
                "|",
                format_value(education.start_year),
                "-",
                format_value(education.end_year),
                "| wiek:",
                format_value(education.age_at_start),
                "|",
                education.status
            )


if __name__ == "__main__":
    main()