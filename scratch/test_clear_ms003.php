<?php
$_POST = array(
    'action' => 'admin_clear_all_signatures',
    'doc_id' => 'SL-POP-ERP-MS-003'
);
$_SERVER['REQUEST_METHOD'] = 'POST';
$_SESSION['authenticated_user'] = 'ajit@sandslab.com';

include __DIR__ . '/../SL-POP-ERP-MS-003.html';
