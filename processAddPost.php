<?php
$username = $_POST["username"];
$stream = $_POST["stream"];
$message = $_POST["message"];

exec("./stream/post $stream $username MESSAGE_TEXT $message", $status);

echo "Currently logged in as: $username<br>";
exec("./sc header.wpml NULL_STREAM NULL_MSG $username", $header);
foreach($header as $line) {
    echo "$line";
}
exec("./sc addPost.wpml NULL_STREAM NULL_MSG $username", $return);
foreach($return as $line) {
    echo "$line";
}
foreach($status as $line) {
    echo "$line";
}
?>
