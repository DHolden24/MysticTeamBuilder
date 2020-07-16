import itertools
import pickle

def load_raw_teams(file):
    teams = []
    with open(file, 'rb') as f:
        raw_teams = pickle.load(f)

    for t in raw_teams:
        team = list(t)
        if len(set(team)) == 6:
            team.sort()
            teams.append(t)

    unique_teams = set(tuple(t) for t in teams)
    return teams, unique_teams

def write_teams(teams, file):
    f = open(file, 'w')
    for t in teams:
        f.write('\t'.join(t) + '\n')
    f.close()

def write_pivoted_teams(teams, pivots, file):
    f = open(file, 'w')
    for t in teams:
        for p in t:
            temp = [x for x in t if x != p]
            combs = itertools.combinations(temp, 6 - pivots)
            for c in combs:
                f.write(p + '\t' + '\t'.join(c) + '\n')
    f.close()

def find_pairs(teams, file):
    pairs = dict()
    for t in teams:
        for p in t:
            temp = [x for x in t if x != p]
            for i in temp:
                pair = [p, i]
                pair.sort()
                pair = tuple(pair)
                if not pair in pairs.keys():
                    pairs[pair] = 0
                pairs[pair] += 1

    goodPairs = dict()
    for k in pairs.keys():
        if pairs[k] >= 20:
            goodPairs[k] = pairs[k]

    f = open(file, 'w')
    for p in goodPairs:
        f.write('\t'.join(p) + '\t' + str(goodPairs[p]) + '\n')
    f.close()

def write_teams_with_types(teams, file, dexFile):
    typeDict = dict()
    with open(dexFile, encoding="utf8") as f:
        for l in f:
            line = l.rstrip().split('\t')
            typeDict[line[0]] = [t for t in line[1::]]

    f = open(file, 'w')
    for t in teams:
        typesList = [x for types in [typeDict[y] for y in t] for x in types]
        f.write('\t'.join(t) + '\t' + '\t'.join(typesList)+ '\n')
    f.close()

def write_pivoted_teams_with_types(teams, pivots, file, dexFile):
    typeDict = dict()
    with open(dexFile, encoding="utf8") as f:
        for l in f:
            line = l.rstrip().split('\t')
            typeDict[line[0]] = [t for t in line[1::]]

    f = open(file, 'w')
    for t in teams:
        for p in t:
            temp = [x for x in t if x != p]
            combs = itertools.combinations(temp, 6 - pivots)
            for c in combs:
                typesList = [x for types in [typeDict[y] for y in c] for x in types]
                f.write(p + ',' + ' '.join(c) + ' ' + ' '.join(typesList)+ '\n')
    f.close()

def team_types(teams, pivots, file, dexFile):
    typeDict = dict()
    with open(dexFile, encoding="utf8") as f:
        for l in f:
            line = l.rstrip().split('\t')
            typeDict[line[0]] = [t for t in line[1::]]

    f = open(file, 'w')
    for t in teams:
        for p in t:
            temp = [x for x in t if x != p]
            combs = itertools.combinations(temp, 6 - pivots)
            for c in combs:
                typesList = [x for types in [typeDict[y] for y in c] for x in types]
                f.write(' '.join(typeDict[p]) + ',' + ' '.join(typesList)+ '\n')
    f.close()

def pivoted_teams_as_numbers(teams, pivots, file, dexFile):
    numbDict = dict()
    with open(dexFile, encoding="utf8") as f:
        for i, l in enumerate(f):
            line = l.rstrip().split('\t')
            numbDict[line[0]] = str(i)

    f = open(file, 'w')
    for t in teams:
        for p in t:
            temp = [x for x in t if x != p]
            combs = itertools.combinations(temp, 6 - pivots)
            for c in combs:
                numbsList = []
                for x in c:
                    numbsList.append(numbDict[x])
                f.write(numbDict[p] + '\t' + '\t'.join(numbsList) + '\n')
    f.close()

def pivoted_type_numbers(teams, pivots, file, dexFile, typeFile):
    typeDict = dict()
    with open(dexFile, encoding="utf8") as f:
        for l in f:
            line = l.rstrip().split('\t')
            typeDict[line[0]] = [t for t in line[1::]]

    numbDict = dict()
    with open(typeFile) as f:
        for i, l in enumerate(f):
            numbDict[str(l.rstrip())] = str(i)

    f = open(file, 'w')
    for t in teams:
        for p in t:
            temp = [x for x in t if x != p]
            combs = itertools.combinations(temp, 6 - pivots)
            for c in combs:
                numbsList = []
                for x in c:
                    for type in typeDict[x]:
                        numbsList.append(numbDict[type])
                pType = [numbDict[type] for type in typeDict[p]]

                if len(pType) < 2:
                    pType.append(pType[0])

                for i in range((2 * (6 - pivots)) - len(numbsList)):
                    numbsList.append(str(-1))
                f.write('\t'.join(pType) + '\t' + '\t'.join(numbsList) + '\n')
    f.close()

def run():
    teams, uniqueTeams = load_raw_teams("Teams/rawTeams.pkl")
    write_teams(teams, "Teams/teams.txt")
    write_teams(uniqueTeams, "Teams/uniqueTeams.txt")
    find_pairs(teams, "Teams/pairs.txt")
    write_teams_with_types(teams, "Teams/teamsWithTypes.txt", "Dex/sortedNationalDex.txt")
    write_teams_with_types(uniqueTeams, "Teams/uniqueTeamsWithTypes.txt", "Dex/sortedNationalDex.txt")
    for i in range(1, 6):
        write_pivoted_teams(teams, i, "Teams/pivotedTeams" + str(i) + ".txt")
        write_pivoted_teams(teams, i, "Teams/pivotedUniqueTeams" + str(i) + ".txt")
        write_pivoted_teams_with_types(teams, i, "Teams/pivotedTeamsWithTypes" + str(i) + ".txt", "Dex/sortedNationalDex.txt")
        write_pivoted_teams_with_types(uniqueTeams, i, "Teams/pivotedUniqueTeamsWithTypes" + str(i) + ".txt", "Dex/sortedNationalDex.txt")
        team_types(teams, i, "Teams/pivotedTeamTypes" + str(i) + ".txt", "Dex/sortedNationalDex.txt")
        team_types(uniqueTeams, i, "Teams/pivotedUniqueTeamTypes" + str(i) + ".txt", "Dex/sortedNationalDex.txt")
        pivoted_teams_as_numbers(teams, i, "Teams/pivotedTeamNumbers" + str(i) + ".txt", "Dex/sortedNationalDex.txt")
        pivoted_type_numbers(teams, i, "Teams/pivotedTypeNumbers" + str(i) + ".txt", "Dex/sortedNationalDex.txt", "Dex/types.txt")

if __name__ == "__main__":
    run()
