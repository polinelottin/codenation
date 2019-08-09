import os
import hashlib
import requests

from dotenv import load_dotenv
from string import ascii_lowercase
from json import dumps

load_dotenv()

FILENAME = 'answer.json'

def main():
    data = get_data()

    steps = int(data['numero_casas'])
    code = data['cifrado'].lower()

    decoded = decode_data(code, steps)
    data['decifrado'] = decoded
    data['resumo_criptografico'] = get_resumo_criptografico(decoded)

    write_in_file(data)
    post_file()

    print('done!')

def get_data():
    print('fetching data...')

    challenge_api = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'

    url = challenge_api.format(os.getenv("CODENATION_API_KEY"))
    resp = requests.get(url)
    return resp.json()

def decode_data(code, steps):
    print('decoding...')

    LETTERS = {letter: index for index, letter in enumerate(ascii_lowercase, start=1)} 
    reversed_dictionary = dict(map(reversed, LETTERS.items()))

    decifrado = ''

    for letter in code: 
        if(letter in ascii_lowercase):
            letter_position = LETTERS[letter] - steps

            if(letter_position <= 0) :
                letter_position = len(LETTERS) + letter_position

            new_letter = reversed_dictionary[letter_position]
        else:
            new_letter = letter

        decifrado += new_letter

    return decifrado

def get_resumo_criptografico(decoded):
    hsh = hashlib.sha1()
    hsh.update(decoded.encode('utf-8'))
    return hsh.hexdigest()

def write_in_file(data):
    print('writing file...')
 
    data = dumps(data)

    json_file = open(FILENAME, "w+")
    json_file.write(data)
    json_file.close()

def post_file():
    print('posting file...')

    challenge_api = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'
    url = challenge_api.format(os.getenv("CODENATION_API_KEY"))

    with open(FILENAME, 'rb') as data:
        response = requests.post(url, files={'answer': data})

    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    main()