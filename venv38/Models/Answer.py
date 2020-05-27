class Answer:
    answer_text: str = ""
    is_true: bool = False

    def __init__(self, text: str, is_true: bool):
        self.answer_text = text
        self.is_true = is_true
