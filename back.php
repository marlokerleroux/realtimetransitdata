<!DOCTYPE html>
<html>
<head>
   <title>Requête</title>
</head>
<body>
   

   <?php

      $file = fopen("parameter.json", "w");
      $city = $_POST['ville'];
      $bus_stop = $_POST['arret'];

      $string_to_put_into = "{\n
            \"city\":\"" . $city ."\",\n
            \"bus_stop\":\"". $bus_stop."\"\n
         }";
      $fwrite($file, $string_to_put_into);


      fclose($file);
   ?>
</body>
</html>