<?php
$username = $_POST['username'];
$streamChoice = $_POST['streamChoice'];

echo "Currently logged in as: $username";
if((isset($streamChoice)) and ($streamChoice != "NULL_STREAM")) {
    echo ", in Stream: $streamChoice";
}
echo "<br>";
exec("./sc header.wpml NULL_STREAM NULL_MSG $username", $header);
foreach($header as $line) {
    echo "$line";
}
if((isset($streamChoice)) and ($streamChoice != "NULL_STREAM")) {
    exec("./sc home.wpml $streamChoice NULL_MSG $username", $return);
    foreach($return as $line) {
        echo "$line";
    }
    echo "<br>";
    exec("./view.py STREAM_NAME: $streamChoice -1 $username", $displayMsg);
    foreach($displayMsg as $line) {
        echo "$line";
    }
} else {
    echo "Select a Stream to start viewing<br>";
}
?>
