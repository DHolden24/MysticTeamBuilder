import requests
from time import sleep
from bs4 import BeautifulSoup
import pickle
import datetime
from Dex import Dex

host = "https://replay.pokemonshowdown.com"
search_main_format = "/search?user=&format=gen8vgc2021&rating&page={}"
search_similar_formats = ["/search?user=&format=gen8vgc2020&rating&page={}",
                          "/search?user=&format=gen8doublesou&rating&page={}",
                          "/search?user=&format=gen8doublesuu&rating&page={}"]

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

def get_teams(path, page, unique_teams, teams, threshold_date, dex):
    print("Retrieving page {}".format(page))
    response = get_page(page, path)

    soup = BeautifulSoup(response.text, 'html.parser')
    replay_links = soup.findAll("li")[-50:]

    print("{} replays found".format(len(replay_links)))
    for l in replay_links:
        replay_log = get_replay(host + l.a['href'] + '.log')
        date = get_date(host + l.a['href'])

        new_teams = get_teams_from_replay(replay_log)

        if date > threshold_date:
            teams.extend([t for t in new_teams if dex.is_legal_team(t)])

        rating = int(''.join(c for c in l.a.small.text[-5::] if c.isdigit()))
        while rating > 1600:
            teams.extend([t for t in new_teams if dex.is_legal_team(t)])
            rating -= 100

        for t in new_teams:
            t.sort()
            unique_teams.add(tuple(t))

    print("Finished page {}, {} teams collected".format(page, len(unique_teams)))
    return teams, unique_teams

def run(dex, write_loc):
    unique_teams = set()
    teams = []
    threshold_date = (datetime.datetime(2020, 6, 24) - datetime.datetime(1970,1,1)).total_seconds()

    page = 1
    print("Retrieving Main Format Teams: " + search_main_format)
    while page != 26:
        teams, unique_teams = get_teams(search_main_format, page, unique_teams, teams, threshold_date, dex)
        page += 1

    for alt_format in search_similar_formats:
        page = 1
        print("Retrieving Teams from Replay Link: " + alt_format)
        while page != 8:
            teams, unique_teams = get_teams(alt_format, page, unique_teams, teams, threshold_date, dex)
            page += 1


    teams.extend([list(t) for t in unique_teams])
    print("Writing {} sample teams".format(len(teams)))
    write_teams(write_loc, teams)

if __name__=="__main__":
    run(Dex(), "Teams/rawTeams.pkl")