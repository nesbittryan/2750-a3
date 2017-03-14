<?php
$username = $_POST["username"];
$author = $_POST["author"];
$flag = $_POST["flag"];
$streamlist = $_POST["streamlist"];

exec("./stream/addauthor $flag $author $streamlist", $status);

echo "Currently logged in as: $username<br>";
exec("./sc header.wpml NULL_STREAM NULL_MSG $username", $header);
foreach($header as $line) {
    echo "$line";
}
exec("./sc addremoveAuthor.wpml NULL_STREAM NULL_MSG $username", $return);
foreach($return as $line) {
    echo "$line";
}
foreach($status as $line) {
    echo "$line";
}
?>
