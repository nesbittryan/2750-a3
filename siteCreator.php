<html>
<body>
    Creating page from file...
    <?php
        $file = $_POST["file"];
        exec("./sc $file");
    ?>
    DONE!
    <hr>
</body>
</html>
