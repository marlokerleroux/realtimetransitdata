$.getJSON("data/data.json", function (data) {

    $('#ville').change(function () {
        if ($('#ville').val() == "Brest") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.brest, function (index, data) {
                select.append($("<option></option>").attr("value", data.Stop_name).text(data.Stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "Caen") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.caen, function (index, data) {
                select.append($("<option></option>").attr("value", data.stop_name).text(data.stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "Nantes") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.nantes, function (index, data) {
                select.append($("<option></option>").attr("value", data.stop_id).text(data.stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "Rennes") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            var previous = null;
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.rennes, function (index, data) {
                if (previous != data.nom) {
                    select.append($("<option></option>").attr("value", data.nom).text(data.nom));
                }
                previous = data.nom;
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        $('#arret').change(function() {
            if (!$('#arret').val())
              $('#valider').attr('disabled', 'disabled');
            else
              $('#valider').attr('disabled', false);
        });
    });
});

$(document).ready(function () {
    $("#effacer").click(function () {
        $("#container-arrets").empty();
        $('#valider').attr('disabled', 'disabled');
    });

    $('#valider').attr('disabled', 'disabled');
});

$.getJSON( "/opt/projet/parameters.json", function(param) {
    var val = $("<div></div>").text("Arrêt enregistré : "+param.bus_stop+" - Ville : "+param.city);
    $("#val-act").html(val);
});