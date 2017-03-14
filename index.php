<?php
exec("./sc index.wpml NULL_STREAM NULL_MSG none", $return);
foreach($return as $line) {
    echo "$line";
}
?>
