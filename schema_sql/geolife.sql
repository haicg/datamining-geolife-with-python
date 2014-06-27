# Host: 127.0.0.1  (Version: 5.5.37-MariaDB)
# Date: 2014-06-06 15:18:26
# Generator: MySQL-Front 5.3  (Build 4.13)

/*!40101 SET NAMES utf8 */;

#
# Source for table "geolife"
#

CREATE TABLE `geolife` (
  `gps_userid` int(11) DEFAULT NULL,
  `gps_latitude` double DEFAULT NULL,
  `gps_longitude` double DEFAULT NULL,
  `gps_code` int(11) DEFAULT NULL,
  `gps_altitude` double DEFAULT NULL,
  `gps_UTC_timestamp` timestamp NULL DEFAULT NULL,
  `gps_UTC_unix_timestamp` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `unique_key` (`gps_userid`,`gps_latitude`,`gps_longitude`,`gps_code`,`gps_altitude`,`gps_UTC_timestamp`,`gps_UTC_unix_timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=59418621 DEFAULT CHARSET=utf8;

#
# Source for table "staypoint"
#

CREATE TABLE `staypoint` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL DEFAULT '0',
  `arrival_point` int(11) DEFAULT NULL,
  `arrival_timestamp` int(11) DEFAULT NULL,
  `leaving_point` int(11) DEFAULT NULL,
  `leaving_timestamp` int(11) DEFAULT NULL,
  `mean_coordinate_latitude` double DEFAULT NULL,
  `mean_coordinate_longtitude` double DEFAULT NULL,
  `mean_coordinate_altitude` double DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `userid` (`userid`),
  KEY `leaving_point` (`arrival_point`),
  CONSTRAINT `leaving_point` FOREIGN KEY (`arrival_point`) REFERENCES `geolife` (`id`),
  CONSTRAINT `arrivel_point` FOREIGN KEY (`arrival_point`) REFERENCES `geolife` (`id`),
  CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `geolife` (`gps_userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
