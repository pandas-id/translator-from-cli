#!/usr/bin/python

# 2021-08-01

from urllib.request import urlopen
from urllib.parse import quote_plus

import json
import argparse

class GoogleTranslator:
    host = 'https://translate.googleapis.com'

    def __init__(self, sl: str, tl: str):
        self.sl = sl
        self.tl = tl

    def http_get(self, url) -> dict:
        """
        Buat permintaan ke host dan kembalikan
        hasil dalam bentuk json/dictionary
        """

        resp = urlopen(url)
        r = resp.read().decode('utf-8')
        return json.loads(r)

    def generate_url(self, text) -> str:
        """
        Buat url dengan memasukan data berupa: self.sl,
        self.tl, dan text ke dalam template url
        """

        text = quote_plus(text)
        url = (
            self.host +
            f'/translate_a/single?client=gtx&sl={self.sl}&tl={self.tl}&dt=at&dt=bd&dt=ex&' +
            f'dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={text}'
        )

        return url

    def translate(self, text) -> str:
        url = self.generate_url(text)
        obj = self.http_get(url)

        result = ''
        try:
            for x in obj[0]:
                result += x[0]
        except TypeError:
            result = 'NOTE: No definite results'

        return result

if __name__ == "__main__":
    # buat objek ArgumentParser
    parser = argparse.ArgumentParser(
            description='Translate text from Terminal'
    )

    # tambahkan argumen
    parser.add_argument(
            '-sl',
            type=str,
            help="from language [default 'id']",
            default='id')
    parser.add_argument(
            '-tl',
            type=str,
            help="to language [default 'en']",
            default='en')
    parser.add_argument(
            '-f',
            type=str,
            help='text file to be translated',
            action='append')
    parser.add_argument(
            '-tx',
            type=str,
            help='text to be translated',
            nargs='*')
    parser.add_argument(
            '-o',
            type=str,
            help='save result in a file')
    parser.add_argument(
            '-shell',
            help='access the interactive shell',
            action='store_true')


    # jalankan fungsi parse_args()
    args = parser.parse_args()

    # buat objek translator
    translator = GoogleTranslator(args.sl, args.tl)

    result = ''

    if args.shell:
        while True:
            text = input('>> ')
            r = translator.translate(text)
            print(r)

    if args.tx != None:
        text = ' '.join(args.tx)
        r = translator.translate(text)
        result += r
        print(r)

    result += '\n'+'='*50+'\n'
    if args.f != None:
        for fn in args.f:
            with open(fn, 'r') as f:
                r = translator.translate(f.read())
                result += r
                result += '\n'+'='*50+'\n'
                print(f'translation of {fn}\n{"="*50}\n{r}\n\n')

    # save result
    if result != '' and args.o != None:
        with open(args.o, 'w') as f:
            f.write(result)

        print(f'results saved in file {args.o}')
