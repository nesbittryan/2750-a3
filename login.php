<?php
exec('./sc home.wpml', $return);
foreach($return as $line) {
    echo "$line";
}
?>
