<html>
<body>
    Creating page from file...
    <?php
        $file = $_POST["file"];
        exec("./sc $file none");
    ?>
    DONE!
    <hr>
</body>
</html>
