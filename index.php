<?php
exec("./sc index.wpml STREAM_NULL MSG_NULL NAME_NULL", $return);
foreach($return as $line) {
    echo "$line";
}
?>
