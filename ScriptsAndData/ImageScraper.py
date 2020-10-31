import requests
from time import sleep
from os import path

host = "https://play.pokemonshowdown.com/sprites"
pokemon = host + "/ani/"
types = host + "/types/"

with open("../app/static/images/icons/grumpig.png", 'wb') as t:
    t.write(requests.get(host + "/bwicons/326.png").content)

with open("Dex/types.txt") as f:
    for i, l in enumerate(f):
        l = l.rstrip()
        with open("../app/static/images/types/" + l + ".png", 'wb') as t:
            t.write(requests.get(types + l + ".png").content)
        sleep(1)

    print("Done Types")

with open("Dex/legalList.txt") as f:
    for i, l in enumerate(f):
        if i % 50 == 0: print("Done {}".format(i))

        l = l.split("\t")[0].replace(" ", "").replace(".", "").replace(":", "").replace("'", "").lower().replace("o-o", "oo")
        file = "../app/static/images/sprites/" + l + ".gif"

        if not path.exists(file):
            print("Retrieveing gif for " + l)
            try:
                response = requests.get(pokemon + l + ".gif")
            except Exception:
                sleep(5)
                response = requests.get(pokemon + l + ".gif")

            if response.status_code != 404:
                with open(file, 'wb') as t:
                    t.write(response.content)
            else:
                print("Failed to get gif for " + l)


            sleep(2)