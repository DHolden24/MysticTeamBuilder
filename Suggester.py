import pickle
import numpy as np

class Suggester:

    def __init__(self):
        self.teamNets = []
        self.primaryTypeNets = []
        self.secondaryTypeNets = []
        for i in range(1, 6):
            self.teamNets.append(pickle.load(open("NeuralNets/TeamSuggest" + str(i), 'rb')))
            self.primaryTypeNets.append(pickle.load(open("NeuralNets/PrimaryType" + str(i), 'rb')))
            self.secondaryTypeNets.append(pickle.load(open("NeuralNets/SecondaryType" + str(i), 'rb')))

    def get_suggestions(self, selected_mon_list, selected_type_list, dex):
        suggested_mons = dict()
        suggested_types = dict()

        selected_mon_list.sort()

        for i in range(len(selected_mon_list)):
            output = self.teamNets[0].predict_proba([[selected_mon_list[i]]])[0]
            vals = get_top_legal_mons(output, self.teamNets[0].classes_, dex)
            add_values_to_dict(vals, suggested_mons)


        output = self.teamNets[len(selected_mon_list) - 1].predict_proba([selected_mon_list])[0]
        vals = get_top_legal_mons(output, self.teamNets[len(selected_mon_list) - 1].classes_, dex)
        add_values_to_dict(vals, suggested_mons)

        output = self.primaryTypeNets[len(selected_mon_list) - 1].predict_proba([selected_type_list])[0]
        vals = get_top_values(output, self.primaryTypeNets[len(selected_mon_list) - 1].classes_)
        add_values_to_dict(vals, suggested_types)

        output = self.secondaryTypeNets[len(selected_mon_list) - 1].predict_proba([selected_type_list])[0]
        vals = get_top_values(output, self.secondaryTypeNets[len(selected_mon_list) - 1].classes_)
        add_values_to_dict(vals, suggested_types)

        return [(m, int(s * 1000) / 1000) for m, s in sorted(suggested_mons.items(), key=lambda item: -item[1]) if m not in selected_mon_list], \
               [(t, int(s * 1000) / 1000) for t, s in sorted(suggested_types.items(), key=lambda item: -item[1])]

def get_top_legal_mons(output, labels, dex, number=5):
    values = sorted(get_top_values(output, labels, 3 * number), key=lambda item: -item[1])
    return_values = set()

    for (mon, score) in values:
        if dex.is_legal(mon):
            return_values.add((mon, score))

        if len(return_values) >= number:
            break

    return return_values

def get_top_values(output, labels, number=5, min_value=0.005):
    number = min([len(output), number])
    values = set()

    while len(values) < number:
        maximum = np.amax(output)
        if maximum < min_value:
            return values

        max_indices = np.where(output == maximum)

        for j in max_indices:
            values.add((labels[j][0], maximum))
            output[j] = 0.
    return values

def add_values_to_dict(values, dictionary):
    for p, s in values:
        p = int(p)
        if p not in dictionary.keys():
            dictionary[p] = s
        else:
            dictionary[p] += s

if __name__=='__main__':
    sgstr = Suggester()

    print(sgstr.get_suggestions([87, 101, 256, 354, 388], [7, 13, 15, 13, 2, 16, 4, 5, 16, -1]))
