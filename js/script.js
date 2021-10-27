$.getJSON("data/data.json", function (data) {

    $('#ville').change(function () {
        if ($('#ville').val() == "brest") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.brest, function (index, data) {
                select.append($("<option></option>").attr("value", data.Stop_name).text(data.Stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "caen") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.caen, function (index, data) {
                select.append($("<option></option>").attr("value", data.fields.stop_name).text(data.fields.stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "nantes") {
            var select = $("<select></select>").attr("id", "arret").attr("name", "arret").attr("class", "form-control");
            select.append($("<option disabled selected value> -- Aucun -- </option>"));
            $.each(data.nantes, function (index, data) {
                select.append($("<option></option>").attr("value", data.fields.stop_id).text(data.fields.stop_name));
            });
            $("#container-arrets").html(select).append("<label>Choix de l'arrêt</label>");
        }
        if ($('#ville').val() == "rennes") {
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
    });
});

$(document).ready(function () {
    $("#effacer").click(function () {
        $("#container-arrets").empty();;
    });
});