<!doctype html>
<html lang="fr">

<head>
  <meta charset="utf-8">
  <title>Projet Python</title>
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="css/style.css">
  <script type="text/javascript" src="js/bootstrap.min.js"></script>
  <script type="text/javascript" src="js/jquery-3.6.0.min.js"></script>
  <script type="text/javascript" src="js/script.js"></script>
</head>

<body class="text-center">
  <div class="modal-dialog" role="document">
    <div class="modal-content rounded-5 shadow">
      <div class="modal-header p-5 pb-4 border-bottom-0">
        <h2 class="fw-bold mb-0">Horaires bus</h2>
      </div>

      <div class="modal-body p-5 pt-0">
      <div id="val-act" class="alert alert-info" role="alert">
      <?php
        $strJsonFileContents = file_get_contents("/opt/projet/parameters.json");
        $array = json_decode($strJsonFileContents);
        $result = $array->bus_stop;
        echo "Arrêt enregistré : ";
        echo $result;
        $result = $array->city;
        echo " - Ville : ";
        echo $result;
      ?>
      </div>
        <form action="<?php echo $_SERVER['PHP_SELF'];?>" method="POST">
          <div class="form-floating mb-3">
            <select id="ville" name="ville" class="form-control">
              <option disabled selected value> -- Aucune -- </option>
              <option value="Brest">Brest</option>
              <option value="Caen">Caen</option>
              <option value="Nantes">Nantes</option>
              <option value="Rennes">Rennes</option>
            </select>
            <label>Choix de la ville</label>
          </div>
          <div id="container-arrets" class="form-floating mb-3"></div>
          <button id="valider" class="col-5 mb-2 btn btn-lg rounded-4 btn-success" type="submit">Enregistrer</button>
          <button id="effacer" class="col-5 mb-2 btn btn-lg rounded-4 btn-danger" type="reset">Effacer</button>
        </form>
      </div>
    </div>
  </div>
</body>

<?php

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $file = fopen("/opt/projet/parameters.json", "w");
      $city = $_POST['ville'];
      $bus_stop = $_POST['arret'];

      $string_to_put_into = "{\n
            \"city\":\"" . $city ."\",\n
            \"bus_stop\":\"". $bus_stop."\"\n
         }";
      $fwrite = fwrite($file, $string_to_put_into);
      fclose($file);
      header("Refresh:0");
  } 
   ?>

  

</html>