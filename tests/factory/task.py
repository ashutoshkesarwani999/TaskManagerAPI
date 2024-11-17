from random import choice, randint

from faker import Faker

from app.schemas.request import TaskCreateRequest

fake = Faker()


def create_fake_task(
    id: int = None, title: str = None, description: str = None, completed: bool = None
):
    return {
        "id": id if id is not None else randint(1, 1000),
        "title": (
            title
            if title is not None
            else fake.sentence(nb_words=6, variable_nb_words=True).rstrip(".")
        ),
        "description": (
            description
            if description is not None
            else fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
        ),
        "completed": completed if completed is not None else choice([True, False]),
    }
