<?php
if($argc != 3) {
    echo "\$key \$server\n";
    die();
}

$servers = array();

$servers[0] = new Memcache;
$servers[1] = new Memcache;

$servers[0]->addServer('10.0.1.6', 11211);
$servers[1]->addServer('10.0.1.7', 11211);

$i = $argv[1];
$server = $argv[2];
echo $servers[$server]->get(md5($i))."\n";