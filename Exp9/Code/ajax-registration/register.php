<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $name = $_POST["name"];
  $college = $_POST["college"];
  $username = $_POST["username"];
  $password = $_POST["password"];

  // Simulate saving data to DB
  echo "Successfully Registered!";
}
?>
