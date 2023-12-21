import json
import unicodedata


class Genderify(object):
    def __init__(self, filename="", ambiguousness=0.02):
        try:
            self.match_list = json.load(open(filename))
        except FileNotFoundError:
            self.match_list = {}

        self.ambiguousness = ambiguousness

    @staticmethod
    def lowercase_and_normalise(name):
        name = unicodedata.normalize("NFKD", str(name))
        return name.encode("ascii", errors="ignore").decode("utf-8").lower()

    @staticmethod
    def gender_from_ratio(ratio, ambiguousness):
        if ratio >= 1 - (ambiguousness / 2):
            return "F"
        elif ratio <= ambiguousness / 2:
            return "M"
        else:
            return "A"

    def gender(self, name, ambiguousness=None):
        if not ambiguousness:
            ambiguousness = self.ambiguousness

        name = Genderify.lowercase_and_normalise(name)

        if name not in self.match_list:
            return

        return self.gender_from_ratio(self.match_list[name], ambiguousness)

    def ratio(self, name):
        name = Genderify.lowercase_and_normalise(name)

        if name not in self.match_list:
            return

        return self.match_list[name]
