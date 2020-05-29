class Question:

    def __init__(self, text: list):
        self.question = str(text[0])
        self.answers = []
        self.size = 0

        for i in range(1, len(text)):
            self.size += 1
            self.answers.append(str(text[i]))

    def show(self) -> str:
        result = "\t\'" + self.question + "\'\n"
        for ans in self.answers:
            result += str(ans) + "\n"

        return result
