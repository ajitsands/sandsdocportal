<?php
$_POST = array(
    'action' => 'submit_signature',
    'doc_id' => 'SL-POP-ERP-MS-003',
    'signer_org' => 'SaNDS Lab Middle East W.L.L',
    'signer_role' => 'Lead Solution Architect',
    'signer_email' => 'ajit@sandslab.com',
    'signer_name' => 'Ajit Kumar KV',
    'signature_data' => 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
);
$_SERVER['REQUEST_METHOD'] = 'POST';
$_SESSION['authenticated_user'] = 'ajit@sandslab.com';

include __DIR__ . '/../SL-POP-ERP-MS-003.html';