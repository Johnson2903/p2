<?php
// index.php

// Define the Python script and the virtual environment's Python interpreter
$pythonScript = '/Applications/XAMPP/xamppfiles/htdocs/ck/cookies.py';
$venvPython = '/Applications/XAMPP/xamppfiles/htdocs/ck/myenv/bin/python';

// Execute the Python script using the virtual environment's Python interpreter
$output = shell_exec("$venvPython $pythonScript");

// Output the result (if any)
echo "<pre>$output</pre>";
?>
