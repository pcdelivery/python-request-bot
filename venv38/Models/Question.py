class Question:

    def __init__(self, text: list):
        # print("QUESTION: " + str(text) + " : " + str(len(text)))

        self.question = str(text[0])
        self.answers = []
        self.size = 0

        for i in range(1, len(text)):
            # print("QUESTION APPEND: " + text[i])

            self.size += 1
            # print("ANSWER: " + str(text[i]))
            self.answers.append(str(text[i]))

        # print("QUESTION ANSWERS LEN: " + str(len(self.answers)))

    def show(self) -> str:
        result = "\t\'" + self.question + "\'\n"
        # print("Question Text: " + self.question)
        for ans in self.answers:
            result += str(ans) + "\n"

        return result
