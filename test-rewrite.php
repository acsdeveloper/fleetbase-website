<?php
if (function_exists('apache_get_modules')) {
    $modules = apache_get_modules();
    if (in_array('mod_rewrite', $modules)) {
        echo "✓ mod_rewrite IS ENABLED\n";
    } else {
        echo "✗ mod_rewrite is NOT enabled\n";
        echo "Enabled modules:\n";
        foreach ($modules as $module) {
            echo "  - $module\n";
        }
    }
} else {
    echo "Cannot check modules - apache_get_modules() not available\n";
}
?>
