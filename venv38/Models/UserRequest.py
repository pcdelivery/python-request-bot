import re
from venv38.Models.Question import Question

# ([+-]) - plus/minus
# [^:+-]([\w\s]+) - only phrases

class UserRequest:
    place_title: str = ""
    description: str = ""
    questions = []
    size: int = 0

    # def __init__(self, place: str, description: str):
    #     self.place_title = place
    #     self.description = description


    # def __init__(self, regex: str):
    #     # examples: "This one ", "another one"
    #     phrases = re.findall("[^:+-]([\w\s]+)", regex)
    #
    #     # pluses and minuses
    #     answer_tags = re.findall("([+-])", regex)
    #
    #     self.description = phrases[0]
    #     self.place_title = phrases[1]

    def add_question(self, question: Question):
        self.questions[self.size] = question
        self.size += 1
