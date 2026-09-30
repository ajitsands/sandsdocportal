<?php
$_SERVER['REQUEST_METHOD'] = 'POST';
$_POST['action'] = 'sign_document';
$_POST['doc_id'] = 'SL-POP-ERP-ARCH-001';
$_POST['signature_data'] = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
$_POST['signer_name'] = 'Test Signer';
$_POST['signer_org'] = 'Popular Auto Spare';
$_POST['signer_role'] = 'Director';

ob_start();
include __DIR__ . '/../SL-POP-ERP-ARCH-001.html';
$out = ob_get_clean();

echo "Length: " . strlen($out) . "\n";
echo "First 100 chars: " . substr($out, 0, 100) . "\n";
?>
