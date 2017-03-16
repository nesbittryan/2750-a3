<?php
$username = $_POST["username"];
$author = $_POST["author"];
$flag = $_POST["flag"];
$streamlist = $_POST["streamlist"];

exec("./stream/addauthor $flag $author $streamlist", $status);

echo "Currently logged in as: $username<br>";
exec("./sc header.wpml STREAM_NULL MSG_NULL $username", $header);
foreach($header as $line) {
    echo "$line";
}
exec("./sc addremoveAuthor.wpml STREAM_NULL MSG_NULL $username", $return);
foreach($return as $line) {
    echo "$line";
}
foreach($status as $line) {
    echo "<br>$line";
}
?>
