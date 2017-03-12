<?php
$username = $_POST['username'];
echo "Currently logged in as: $username<br>";
exec("./sc addPost.wpml $username", $return);
foreach($return as $line) {
    echo "$line";
}
?>
