from venv38.Models.Answer import Answer


class Question:
    question: str = ""
    answers = []
    size: int = 0

    def __init__(self, text: str):
        self.question = text

    def add_answer(self, answer: Answer):
        self.answers[self.size] = Answer
        self.size += 1
