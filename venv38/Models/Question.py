from venv38.Models.Answer import Answer


class Question:
    question: str = ""
    answers = []
    size: int = 0

    def __init__(self, text: list):
        # print("QUESTION: " + str(text) + " : " + str(len(text)))

        self.question = str(text[0])
        self.answers = []

        for i in range(1, len(text)):
            # print("QUESTION APPEND: " + text[i])

            self.size += 1
            # print("ANSWER: " + str(text[i]))
            self.answers.append(str(text[i]))

        # print("QUESTION ANSWERS LEN: " + str(len(self.answers)))

    def show(self) -> str:
        result = "\'" + self.question + "\'"
        # print("Question Text: " + self.question)
        for ans in self.answers:
            result += str(ans) + "\n"

        return result
