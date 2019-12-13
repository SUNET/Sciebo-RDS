<?php
namespace OCA\RDS\AppInfo;

use \OCP\AppFramework\App;
use \OCA\RDS\Controller\PageController;
use \OCA\RDS\Controller\ServiceController;

class Application extends App {
    public function __construct(array $urlParams=array()){
        parent::__construct('rds', $urlParams);

        $container = $this->getContainer();
        
        $container->registerService('PageController', function($c) {
            return new PageController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query('OCA\OAuth2\Db\ClientMapper'),
                $c->query('UserId')
            );
        });

        $container->registerService('ServiceController', function($c) {
            return new ServiceController(
                $c->query('AppName'),
                $c->query('Request'),
                $c->query('UserId')
            );
        });
    }
}
