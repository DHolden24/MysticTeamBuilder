from sklearn.neural_network import MLPClassifier
import numpy as np
import pickle

def build_team_nets(dataFile, pickleFile):
    for i in range(1, 6):
        team_array = np.genfromtxt(dataFile + str(i) + '.txt', delimiter="\t")

        y = team_array[:, 0]
        x = np.delete(team_array, 0, 1)

        clf = MLPClassifier(solver='lbfgs', alpha=1e-7, hidden_layer_sizes=(200, 200, 200), max_iter=2000,
                            activation='relu',
                            learning_rate='invscaling', shuffle=True, early_stopping=False)

        clf.fit(x, y)
        with open(pickleFile + str(6 - i), 'wb') as f:
            pickle.dump(clf, f)
        print("Done team net {}".format(i))

def build_type_teams(dataFile, primaryPickleFile, secondaryPickleFile):
    for i in range(1, 6):
        team_array = np.genfromtxt(dataFile + str(i) + '.txt', delimiter="\t")

        y1 = team_array[:, 0]
        y2 = team_array[:, 1]
        x = np.delete(team_array, (0, 1), 1)

        clf1 = MLPClassifier(solver='adam', alpha=1e-4, hidden_layer_sizes=(50, 75, 50, 25), max_iter=775, shuffle=True,
                             learning_rate='constant', early_stopping=False)
        clf1.fit(x, y1)
        with open(primaryPickleFile + str(6 - i), 'wb') as f:
            pickle.dump(clf1, f)

        clf2 = MLPClassifier(solver='lbfgs', alpha=1e-6, hidden_layer_sizes=(25, 100, 50, 25), max_iter=2050,
                             learning_rate='invscaling')

        clf2.fit(x, y2)
        with open(secondaryPickleFile + str(6 - i), 'wb') as f:
            pickle.dump(clf2, f)
        print("Done type net {}".format(i))

if __name__=="__main__":
    build_team_nets("ScriptsAndData/Teams/pivotedTeamNumbers", "NeuralNets/TeamSuggest")
    build_type_teams("ScriptsAndData/Teams/pivotedTypeNumbers", "NeuralNets/PrimaryType", "NeuralNets/SecondaryType")


