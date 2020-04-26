import unicodedata
class unicodeToString:
    def unicodeToString(self, data):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')