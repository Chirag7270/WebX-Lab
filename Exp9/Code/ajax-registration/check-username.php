<?php
$existingUsers = ["john", "doe", "admin"]; // Simulated database

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $username = $_POST["username"];
  if (in_array(strtolower($username), $existingUsers)) {
    echo "Username already taken.";
  } else {
    echo "Username available.";
  }
}
?>
