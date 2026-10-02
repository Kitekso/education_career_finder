from models import Education, Person


def get_record_value(record: dict, key: str) -> str | None:
    field = record.get(key)

    if field is None:
        return None

    return field.get("value")


def get_year(record: dict, key: str) -> int | None:
    value = get_record_value(record, key)

    if value is None:
        return None

    try:
        return int(value[:4])
    except ValueError:
        return None


def get_wikidata_id(entity_url: str) -> str:
    return entity_url.rsplit("/", 1)[-1]


def build_people(records: list[dict]) -> dict[str, Person]:
    people: dict[str, Person] = {}

    for record in records:
        person_url = get_record_value(record, "person")

        if person_url is None:
            continue

        wikidata_id = get_wikidata_id(person_url)

        if wikidata_id not in people:
            person_name = get_record_value(record, "personLabel")
            birth_year = get_year(record, "birthDate")

            people[wikidata_id] = Person(
                name=person_name or wikidata_id,
                wikidata_id=wikidata_id,
                birth_year=birth_year
            )

        education = Education(
            university=get_record_value(record, "universityLabel"),
            major=get_record_value(record, "majorLabel"),
            degree=get_record_value(record, "degreeLabel"),
            start_year=get_year(record, "startDate"),
            end_year=get_year(record, "endDate"),
            status="studied"
        )

        people[wikidata_id].add_education(education)

    return people


def filter_people_with_min_majors(
    people: dict[str, Person],
    min_majors: int = 2
) -> list[Person]:

    results = []

    for person in people.values():
        if person.get_number_of_majors() >= min_majors:
            results.append(person)

    results.sort(
        key=lambda person: person.get_number_of_majors(),
        reverse=True
    )

    return results