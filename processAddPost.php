<?php
$username = $_POST["username"];
$stream = $_POST["stream"];
$message = $_POST["message"];

exec("./stream/post $stream $username MESSAGE_TEXT $message", $status);

echo "Currently logged in as: $username<br>";
exec("./sc addPost.wpml $username", $return);
foreach($return as $line) {
    echo "$line";
}
foreach($status as $line) {
    echo "$line";
}
?>
