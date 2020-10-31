import ScriptsAndData.ReplayScraper as rs
import ScriptsAndData.TeamMunger as tm
from Dex import Dex
import ClassifierBuilder

if __name__=="__main__":
    dex = Dex()

    rs.run(dex, "ScriptsAndData/Teams/rawTeams.pkl")
    tm.run("ScriptsAndData/Teams/", "ScriptsAndData/Dex/")

    ClassifierBuilder.build_team_nets("ScriptsAndData/Teams/pivotedTeamNumbers", "Classifiers/TeamSuggest")
    ClassifierBuilder.build_type_teams("ScriptsAndData/Teams/pivotedTypeNumbers", "Classifiers/PrimaryType", "Classifiers/SecondaryType")