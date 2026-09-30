<?php
session_start();
$_SESSION['authenticated_user'] = 'ajit@sandslab.com';
$_SESSION['auth_role'] = 'Super Admin';
include __DIR__ . '/../index.php';