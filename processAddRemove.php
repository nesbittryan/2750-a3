<?php
$author = $_POST["author"];
$flag = $_POST["flag"];
$streamlist = $_POST["streamlist"];
echo "AUTHOR: $author<br>";
echo "FLAG: $flag<br>";
echo "streams: $streamlist<br>";
exec("./stream/addauthor $flag $author $streamlist");
header('Location: login.php');
exit(1);
?>
