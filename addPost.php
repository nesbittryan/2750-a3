<?php
$username = $_POST['username'];
$username = "Ryan";

exec("./sc header.wpml STREAM_NULL MSG_NULL $username", $header);
foreach($header as $line) {
    echo "$line";
}

exec("./sc addPost.wpml STREAM_NULL MSG_NULL $username", $return);
foreach($return as $line) {
    echo "$line";
}
?>
