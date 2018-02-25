import requests
from os import path


class QuranTafseerService:
    BASE_URL = 'http://api.quran-tafseer.com/tafseer/'

    @classmethod
    def ayah_tafseer(cls, chapter_number, ayah_number, tafseer_number):
        last_part = '{}/{}/{}'.format(tafseer_number,
                                      chapter_number,
                                      ayah_number)

        url = path.join(cls.BASE_URL, last_part)
        tafseer_response = requests.get(url)
        if tafseer_response.status_code != 200:
            return 'Something went wrong'
        return tafseer_response
