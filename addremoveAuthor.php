<?php
exec("./sc addremoveAuthor.wpml", $return);
foreach($return as $line) {
    echo "$line";
}
?>
