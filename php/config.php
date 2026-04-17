<?php
require 'class-http-request.php';
require 'functions.php';

$api = "bot306481667:AAFJhVcOXcOl8uz2XrOP6RSdvaa8sRifnoc";

//Connection to Database.
$database = new mysqli("localhost", "wond_erse", "GjKIt+DfjHvLoKev", "wond_erse");

//Other.
$table = "BurningBot";
$canalelog = "-1001122007874";
$canalesegnalazioni = "-1001204753839";
$linkpaypal = "alla mail universeacco@gmail.com";
$admins = array(148959990, 304873904, 31507896,234941898,7511300374);

$ipzsat = "193.37.213.148";


$costoIPTV[1] = 1000;
$costoIPTV[3] = 2500;
$costoIPTV[6] = 4500;
$costoIPTV[12] = 8500;
//$costoIPTV[2] = 1500;

$costoIPTV_New[1] = 1000;
$costoIPTV_New[3] = 2500;
$costoIPTV_New[6] = 4500;
$costoIPTV_New[12] = 8500;

$costoPLEX[1] = 600;
$costoPLEX[4] = 2100;
$costoPLEX[12] = 5000;

$costoVPNII[1] = 200;
$costoVPNII[6] = 1000;
$costoVPNII[12] = 1600;

$costoVPNH[1] = 200;
$costoVPNH[6] = 1000;
$costoVPNH[12] = 1600;

function link_lista($username, $password){
  return "http://wonderse.v6.army:25461/get.php?username=$username&password=$password&type=m3u_plus&output=ts";
}

function link_lista_Anonymous($username, $password){
  $password = trim($password);
  $password = str_replace(" ", "", $password);
  $password = urlencode($password);
  return "http://app.cloud-worker.xyz/get.php?username=$username&password=$password&type=m3u_plus&output=ts";
}


