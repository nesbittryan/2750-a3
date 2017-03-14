<?php
$username = $_POST['username'];
$streamChoice = $_POST['streamChoice'];
echo "Currently logged in as: $username<br>";
exec("./sc header.wpml NULL_STREAM NULL_MSG $username", $header);
foreach($header as $line) {
    echo "$line";
}


?>
