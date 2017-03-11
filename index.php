<?php

exec("./sc index.wpml", $return);
foreach($return as $line) {
    echo "$line";
}
 ?>
