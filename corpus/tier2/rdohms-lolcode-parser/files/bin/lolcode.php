#!/usr/bin/env php
<?php

foreach (array(
             __DIR__ . '/../../../autoload.php',
             __DIR__ . '/vendor/autoload.php',
             __DIR__ . '/../vendor/autoload.php',
             __DIR__ . '/../autoload.php',
         ) as $file) {
    if (file_exists($file)) {
        define('DMS_LOLCODE_COMPOSER_AUTOLOAD', $file);
        break;
    }
}

if (!defined('DMS_LOLCODE_COMPOSER_AUTOLOAD')) {
    die(
        'You need to set up the project dependencies using the following commands:' . PHP_EOL .
        'wget http://getcomposer.org/composer.phar' . PHP_EOL .
        'php composer.phar install' . PHP_EOL
    );
}

require DMS_LOLCODE_COMPOSER_AUTOLOAD;

use DMS\LOL\Command\LolCodeCommand;
use Symfony\Component\Console\Application;

$application = new Application();
$application->add(new LolCodeCommand());
$application->run();
