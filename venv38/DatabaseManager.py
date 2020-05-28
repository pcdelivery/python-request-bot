from venv38.Models.UserRequest import UserRequest

REQUEST_QUE_TABLE = "requests_questions"
REQUEST_ANS_TABLE = "requests_answers"


def text_storing(request: UserRequest):
    with open("data/new_data.txt", "a") as file:
        file.write(request.show())
