function getSuggestions() {
    var team = [];
    var noneCount = 0;

    len = $(".pokemonSelect").length;
    for (i = 0; i < len; i++) {
        var c = $(".pokemonSelect")[i]
        team.push(c.options[c.selectedIndex].value);

        var id = $(".pokemonSelect")[i].id.replace("p", "i");
        if (c.selectedIndex != 0) {
            noneCount += 1;
            $("#".concat(id))[0].src = "../static/images/sprites/".concat(c.options[c.selectedIndex].value.toLowerCase().replace(".", "").replace(" ", ""), ".gif");
            $("#".concat(id))[0].alt = c.options[c.selectedIndex].value;
        } else {
            $("#".concat(id))[0].src = "";
            $("#".concat(id))[0].alt = "";
        };
    };

    if (noneCount == 6) {
        $("#inputConfirm")[0].disabled = true;
    } else {
        $("#inputConfirm")[0].disabled = false;
    };

    var jsonObj = {"team": team}

    $.ajax({
        url: "getSuggestions",
        data: JSON.stringify(jsonObj),
        dataType: 'json',
        contentType: 'application/json',
        type: 'POST',
        success: function(result, status, jqXHR) {
            const pokemon_div = $(".suggestedPokemonImages")[0];
            pokemon_div.innerHTML = "";
            const type_div = $(".suggestedTypeImages")[0];
            type_div.innerHTML = "";

            if (result.note != "None") {
                $("#suggestedPokemonNote")[0].innerHTML = result.note;
                $("#suggestedTypesNote")[0].innerHTML = "";
            } else {
                $("#suggestedPokemonNote")[0].innerHTML = "";
                $("#suggestedTypesNote")[0].innerHTML = "";

                result.pokemon.forEach(function(item, index) {
                    var div = document.createElement("div");
                    div.className += "image_container";
                    pokemon_div.appendChild(div);

                    var img = document.createElement("img");
                    img.src = "../static/images/sprites/".concat(item[0].toLowerCase().replace(".", "").replace(" ", ""), ".gif");
                    img.alt = item[0];
                    img.className += "pokeImage"
                    div.width = img.width
                    div.appendChild(img);

                    var txt = document.createElement("span");
                    txt.innerHTML = item[0].concat("<br>Score: ", item[1]);
                    txt.className += "image_caption"
                    div.appendChild(txt);
                });

                result.types.forEach(function(item, index) {
                var div = document.createElement("div");
                    div.className += "image_container";
                    type_div.appendChild(div);

                    var img = document.createElement("img");
                    img.src = "../static/images/types/".concat(item[0], ".png");
                    img.alt = item[0];
                    div.width = img.width
                    div.appendChild(img);

                    var txt = document.createElement("span");
                    txt.innerHTML = item[0].concat("<br>Score: ", item[1]);
                    txt.className += "image_caption"
                    div.appendChild(txt);
                });
            }
        }
    });
};

function addToTeam() {
    var flag = false;
    var val = -1;
    for (i = 1; i < $(".pokemonSelect")[0].options.length; i++) {
        if ($("#pokeInput")[0].value.toLowerCase() == $(".pokemonSelect")[0].options[i].value.toLowerCase()) {
            flag = true;
            val = i;
            break;
        };
    };

    if (!flag) {
        $("#errorMsg")[0].innerHTML = "Unknown Pokemon. Please ensure that the spelling is correct.";
    } else {
        $("#errorMsg")[0].innerHTML = "";
        len = $(".pokemonSelect").length;
        for (i = 0; i < len; i++) {
            if ($(".pokemonSelect")[i].selectedIndex == 0) {
                $(".pokemonSelect")[i].selectedIndex = val;
                $(".pokemonSelect")[i].onchange();
                break;
            };
        };
    };
};

$( document ).ready(function() {
    $.ajax({
        url: "vgcLegalPokemon",
        success: function(result) {
            len = $(".pokemonSelect").length;
            for (s = 0; s < result.length; s++) {
                for (i = 0; i < len; i++) {
                    var c = $(".pokemonSelect")[i]
                    var option = document.createElement("option");
                    option.value = result[s];
                    option.text = result[s];
                    c.add(option);
                };
            };
        }
    });

    len = $(".pokemonSelect").length;
    for (i = 0; i < len; i++) {
        $(".pokemonSelect")[i].onchange = getSuggestions;
    };

    $("#inputConfirm")[0].onclick = addToTeam;
});