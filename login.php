<?php
$username = $_POST["username"];
echo "Logged in as: $username";
exec('./sc home.wpml', $return);
foreach($return as $line) {
    echo "$line";
}
?>
