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
                select.append($("<option></option>").attr("value", data.fields.stop_name).text(data.fields.stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "Nantes") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.nantes, function (index, data) {
                select.append($("<option></option>").attr("value", data.fields.stop_id).text(data.fields.stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "Rennes") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            var previous = null;
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.rennes, function (index, data) {
                if (previous != data.fields.nom) {
                    select.append($("<option></option>").attr("value", data.fields.nom).text(data.fields.nom));
                }
                previous = data.fields.nom;
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

$.getJSON( "data/parameters.json", function(param) {
    var val = $("<div></div>").text("Arrêt enregistré : "+param.bus_stop+" - Ville : "+param.city);
    $("#val-act").html(val);
});