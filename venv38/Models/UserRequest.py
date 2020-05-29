from venv38.Models.Question import Question

# ([+-]) - plus/minus
# [^:+-]([\w\s]+) - only phrases


class UserRequest:

    def __init__(self, user_id: int, description: str, place: str, questions: list):
        self.user_id = str(user_id)
        self.description = description
        self.place_title = place
        self.questions = []
        self.size = 0
        self.ans_size = 0

        for que in questions:
            self.size += 1

            temp = Question(que)
            self.ans_size += temp.size
            self.questions.append(temp)

    def show(self) -> str:
        result = ""
        result += "\n\n\tUser id: " + str(self.user_id)
        result += "\n\tUserRequest\n\tDescription: " + self.description
        result += "\n\tPlace: " + self.place_title
        result += "\n\tQuestion size: " + str(self.size)
        result += "\n\tAnswers size: " + str(self.ans_size)
        result += "\n\tQuestions:\n"

        for i in range(0, self.size):
            result += self.questions[i].show()

        return result

    def add_question(self, question: Question):
        self.questions[self.size] = question
        self.size += 1
