<?php
$username = $_POST['username'];
echo "Currently logged in as: $username<br>";
exec("./sc header.wpml NULL_STREAM NULL_MSG $username", $header);
foreach($header as $line) {
    echo "$line";
}
exec("./view.py $username", $status);
foreach($status as $line) {
    echo "$line";
}
?>
