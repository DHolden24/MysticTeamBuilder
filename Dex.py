
class Dex:

    def __init__(self):
        self.typeDict = self.NameToNumberMap()
        with open("ScriptsAndData/Dex/types.txt") as f:
            for i, l in enumerate(f):
                self.typeDict.add(i, l.rstrip())

        self.monDict = self.NameToNumberMap()
        self.monTypes = dict()
        with open("ScriptsAndData/Dex/sortedNationalDex.txt", encoding="utf8") as f:
            for i, l in enumerate(f):
                line = l.rstrip().split('\t')
                self.monDict.add(i, line[0])
                self.monTypes[line[0]] = line[1::]

        legal_mons = set()
        with open("ScriptsAndData/Dex/legalList.txt") as f:
            for l in f:
                legal_mons.add(l.rstrip().split('\t')[0])
        self.legal_mons = list(legal_mons)
        self.legal_mons.sort()

    def get_type(self, val):
        return self.typeDict.get(val)

    def get_mon(self, val):
        return self.monDict.get(val)

    def get_mon_type(self, val):
        return self.monTypes.get(val)

    def get_legal_mons(self):
        return self.legal_mons

    def is_legal(self, mon):
        return mon in self.legal_mons or self.get_mon(mon) in self.legal_mons

    def is_legal_team(self, team):
        for t in team:
            if not self.is_legal(t):
                return False
        return True

    class NameToNumberMap:

        def __init__(self):
           self.d = {}

        def add(self, k, v):
           self.d[k] = v
           self.d[v] = k

        def get(self, k):
           return self.d[k]

if __name__ == '__main__':
    dex = Dex()

    print(dex.get_type("fire"))
    print(dex.get_type(2))

    print(dex.get_mon("Umbreon"))
    print(dex.get_mon(172))

    print(dex.get_mon_type("Umbreon"))
