<?php
$_SERVER['REQUEST_METHOD'] = 'POST';
$_POST['action'] = 'admin_clear_signature';
$_POST['doc_id'] = 'SL-POP-ERP-ARCH-001';
$_POST['target_email'] = 'director@popularbahrain.com';

ob_start();
include __DIR__ . '/../SL-POP-ERP-ARCH-001.html';
$out = ob_get_clean();
echo $out;
?>
