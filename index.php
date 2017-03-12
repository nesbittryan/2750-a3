<?php
exec("./sc index.wpml none", $return);
foreach($return as $line) {
    echo "$line";
}
?>
