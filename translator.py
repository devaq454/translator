import googletrans


class Translator:
    def __init__(self):
        self.long_short = dict()
        for short, long in googletrans.LANGUAGES.items():
            self.long_short[long.capitalize()] = short
        self.translator = googletrans.Translator()

    def translate(self, from_language, to_language, from_text):
        result = self.translator.translate(text=from_text, src=self._get_language(from_language),
                                           dest=self._get_language(to_language))
        return result.text

    def _get_language(self, long):
        return self.long_short.get(long)
