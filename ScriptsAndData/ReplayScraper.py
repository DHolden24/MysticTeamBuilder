import requests
from time import sleep
from bs4 import BeautifulSoup
import pickle
import datetime
from Dex import Dex

host = "https://replay.pokemonshowdown.com"
search_vgc = "/search?user=&format=gen8vgc2020&rating&page={}"
search_ou_doubles = "/search?user=&format=gen8doublesou&rating&page={}"
search_uu_doubles = "/search?user=&format=gen8doublesuu&rating&page={}"

def get_page(page, site):
    sleep(10)
    response = None

    while response is None:
        try:
            response = requests.get(host + site.format(page))
        except Exception as e:
            sleep(150)
            response = None

    return response

def get_replay(address):
    sleep(2)
    replay_log = None

    while replay_log is None:
        try:
            replay_log = requests.get(address)
        except Exception:
            sleep(150)
            replay_log = None

    return replay_log

def get_date(address):
    sleep(0.5)
    replay = None

    while replay is None:
        try:
            replay = requests.get(address)
        except Exception:
            sleep(150)
            replay = None

    soup = BeautifulSoup(replay.text, 'html.parser')
    date = soup.findAll("small", {"class": "uploaddate"})[0]['data-timestamp']
    return int(date)

def get_teams_from_replay(replay_log):
    new_teams = [[], []]

    for n in [x for x in replay_log.text.split('\n') if x.startswith("|poke")]:
        pokemon = n.split('|')[3].split(', ')[0]
        pokemon = pokemon.replace("-East", "").replace("-West", "").replace("-*", "").replace("’", "'")

        if pokemon.startswith("Alcremie"):
            pokemon = "Alcremie"

        if n.startswith("|poke|p1"):
            new_teams[0].append(pokemon)
        elif n.startswith("|poke|p2"):
            new_teams[1].append(pokemon)

    return new_teams

def write_teams(file_name, teams):
    with open(file_name, 'wb') as f:
        pickle.dump(teams, f)

def run(dex, write_loc):
    unique_teams = set()
    teams = []
    page = 1
    threshold_date = (datetime.datetime(2020, 6, 24) - datetime.datetime(1970,1,1)).total_seconds()

    print("Retrieving VGC Teams")
    while page != 26:
        print("Retrieving page {}".format(page))
        response = get_page(page, search_vgc)

        soup = BeautifulSoup(response.text, 'html.parser')
        replay_links = soup.findAll("li")[-50:]

        print("{} replays found".format(len(replay_links)))
        for l in replay_links:
            replay_log = get_replay(host + l.a['href'] + '.log')
            date = get_date(host + l.a['href'])

            new_teams = get_teams_from_replay(replay_log)

            if date > threshold_date:
                teams.extend(new_teams)

            rating = int(''.join(c for c in l.a.small.text[-5::] if c.isdigit()))
            while rating > 1600:
                teams.extend(new_teams)
                rating -= 100

            for t in new_teams:
                t.sort()
                unique_teams.add(tuple(t))

        print("Finished page {}, {} teams collected".format(page, len(unique_teams)))
        page += 1

    page = 1
    print("Retrieving OU Doubles Teams")
    while page != 11:
        print("Retrieving page {}".format(page))
        response = get_page(page, search_ou_doubles)

        soup = BeautifulSoup(response.text, 'html.parser')
        replay_links = soup.findAll("li")[-50:]

        print("{} replays found".format(len(replay_links)))
        for l in replay_links:
            replay_log = get_replay(host + l.a['href'] + '.log')

            new_teams = get_teams_from_replay(replay_log)
            new_teams = [t for t in new_teams if dex.is_legal(t)]

            for t in new_teams:
                t.sort()
                unique_teams.add(tuple(t))

        print("Finished page {}, {} teams collected".format(page, len(unique_teams)))
        page += 1

    page = 1
    print("Retrieving UU Doubles Teams")
    while page != 11:
        print("Retrieving page {}".format(page))
        response = get_page(page, search_uu_doubles)

        soup = BeautifulSoup(response.text, 'html.parser')
        replay_links = soup.findAll("li")[-50:]

        print("{} replays found".format(len(replay_links)))
        for l in replay_links:
            replay_log = get_replay(host + l.a['href'] + '.log')

            new_teams = get_teams_from_replay(replay_log)
            new_teams = [t for t in new_teams if dex.is_legal(t)]

            for t in new_teams:
                t.sort()
                unique_teams.add(tuple(t))

        print("Finished page {}, {} teams collected".format(page, len(unique_teams)))
        page += 1

    teams.extend([list(t) for t in unique_teams])
    print("Writing {} sample teams".format(len(teams)))
    write_teams(write_loc, teams)

if __name__=="__main__":
    run(Dex(), "Teams/rawTeams.pkl")