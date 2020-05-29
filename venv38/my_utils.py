import json


def is_moderator(id: int) -> bool:
    try:
        file = open("data/moderators", "r")
        line = "init"

        while line != "":
            line = file.readline()
            # print("is_moderator: line=" + line + " id=" + str(id))
            if int(line) == id:
                print("is_moderator: True")
                return True
    except:
        print("is_moderator: Error")

    print("is_moderator: False")
    return False


def login_moderator(token: str, id: int) -> bool:
    try:
        file = open("data/moderators_auth", "r")
        line = "init"

        while line != "":
            line = file.readline()
            print("is_moderator: line=" + line + " login=" + token)
            if line == token:
                print("is_moderator: True")
                add_moderator(str(id))
                return True
    except:
        print("is_moderator: Error")

    print("is_moderator: False")
    return False


def add_moderator(id):
    try:
        file = open("data/moderators", "a")
        file.write(str(id) + "\n")
    except:
        print("Error while adding new moderator")


def get_phrase_from_res(tag, user_lang_code):
    print(f"[get_phrase_from_res: tag {tag}, user_lang: {user_lang_code}]")

    with open("data/inter_lang.json", "r") as json_file:
        data = json.load(json_file)
        try:
            return data['phrases'][tag][user_lang_code]
        except:
            return data['phrases'][tag]['en']