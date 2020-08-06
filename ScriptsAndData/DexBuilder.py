import yaml

def build_dexes():
    with open("Dex/showdownDex.json", encoding="utf8") as f:
        json_dex = yaml.load(f, Loader=yaml.FullLoader)

    dex = []
    for k in json_dex.keys():
        if k == "missingno": break
        dex.append(json_dex[k]['name'] + '\t' + '\t'.join(json_dex[k]['types']))

    with open("Dex/nationalDex.txt", 'w', encoding="utf8") as f:
        f.write('\n'.join(dex))

    dex.sort()
    with open("Dex/sortedNationalDex.txt", 'w', encoding="utf8") as f:
        f.write('\n'.join(dex))

if __name__=="__main__":
    build_dexes()
