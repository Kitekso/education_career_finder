class Education:
    def __init__(
        self,
        university: str,
        major: str,
        degree: str | None = None,
        start_year: int | None = None,
        end_year: int | None = None,
        age_at_start: int | None = None,
        status: str = "unknown"
    ):
        self.university = university
        self.major = major
        self.degree = degree
        self.start_year = start_year
        self.end_year = end_year
        self.age_at_start = age_at_start
        self.status = status


class Person:
    def __init__(
        self,
        name: str,
        wikidata_id: str,
        birth_year: int | None = None,
        wikipedia_url: str | None = None
    ):
        self.name = name
        self.wikidata_id = wikidata_id
        self.birth_year = birth_year
        self.wikipedia_url = wikipedia_url
        self.educations: list[Education] = []

    def add_education(self, education: Education):
        if (
            self.birth_year is not None
            and education.start_year is not None
        ):
            education.age_at_start = (
                education.start_year - self.birth_year
            )

        self.educations.append(education)

    def get_unique_majors(self) -> set[str]:
    majors: set[str] = set()

    for education in self.educations:
        if education.major is not None:
            majors.add(education.major)

    return majors

    def get_completed_majors(self) -> set[str]:
    completed_majors: set[str] = set()

    for education in self.educations:
        if (
            education.status == "completed"
            and education.major is not None
        ):
            completed_majors.add(education.major)

    return completed_majors


    def get_number_of_majors(self) -> int:
        return len(self.get_unique_majors())

    def get_number_of_completed_majors(self) -> int:
        return len(self.get_completed_majors())