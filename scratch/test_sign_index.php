<?php
$_SERVER['REQUEST_METHOD'] = 'POST';
$_POST['action'] = 'sign_document';
$_POST['doc_id'] = 'SL-POP-ERP-ARCH-001';
$_POST['signature_data'] = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
$_POST['signer_name'] = 'Managing Director';
$_POST['signer_org'] = 'Popular Auto Spare & A/C Parts Co. W.L.L';
$_POST['signer_role'] = 'Executive Sponsor';

ob_start();
include __DIR__ . '/../index.php';
$out = ob_get_clean();
echo $out;
?>
