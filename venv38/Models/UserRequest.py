from venv38.Models.Question import Question


class UserRequest:
    place_title: str = ""
    description: str = ""
    questions = []
    size: int = 0

    def __init__(self, place: str, description: str):
        self.place_title = place
        self.description = description

    def add_question(self, question: Question):
        self.questions[self.size] = question
        self.size += 1
