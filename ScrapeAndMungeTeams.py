import ScriptsAndData.ReplayScraper as rs
import ScriptsAndData.TeamMunger as tm
from Dex import Dex
import NetBuilder

if __name__=="__main__":
    dex = Dex()

    rs.run(dex, "ScriptsAndData/Teams/rawTeams.pkl")
    tm.run("ScriptsAndData/Teams/", "ScriptsAndData/Dex/")

    NetBuilder.build_team_nets("ScriptsAndData/Teams/pivotedTeamNumbers", "NeuralNets/TeamSuggest")
    NetBuilder.build_type_teams("ScriptsAndData/Teams/pivotedTypeNumbers", "NeuralNets/PrimaryType", "NeuralNets/SecondaryType")