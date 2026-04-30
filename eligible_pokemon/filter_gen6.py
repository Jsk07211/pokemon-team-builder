import json
import requests
import time
import re

URL_REGEX = r"https:\/\/pokeapi\.co\/api\/v2\/generation\/(?P<gen>[0-9]+)\/"

with open("eligible_pokemon.json", mode="r") as f:
    with open("eligible_gen_pokemon.json", mode="w") as f_out:
        pokemon = json.load(f)

        for mon in pokemon.keys():
            print(f"Checking {mon}...")
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{mon}/")

            if res.status_code == 200:
            #     res = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{mon}/")

                data = res.json()
                match = re.match(URL_REGEX, data["generation"]["url"])

                if match:
                    gen = int(match.group("gen"))

                    if gen < 7:
                        print(f"Adding {mon}...")
                        f_out.write(f"{mon}\n")

            time.sleep(2)