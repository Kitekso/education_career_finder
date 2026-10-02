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

    return int(value[:4])

def build_people(records: list[dict]) -> dict[str, Person]:
    people: dict[str, Person] = {}

    for record in records:
        person_url = get_record_value(record, "person")

        if person_url is None:
            continue

        wikidata_id = person_url.rsplit("/", 1)[-1]

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