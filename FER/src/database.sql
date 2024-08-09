/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 5.1.32-community : Database - emotion
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`emotion` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `emotion`;

/*Table structure for table `emotions` */

DROP TABLE IF EXISTS `emotions`;

CREATE TABLE `emotions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eid` int(11) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `angry` varchar(11) DEFAULT NULL,
  `disgust` varchar(11) DEFAULT NULL,
  `fear` varchar(11) DEFAULT NULL,
  `happy` varchar(11) DEFAULT NULL,
  `sad` varchar(11) DEFAULT NULL,
  `surprise` varchar(11) DEFAULT NULL,
  `neutral` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `emotions` */

insert  into `emotions`(`id`,`eid`,`date`,`time`,`angry`,`disgust`,`fear`,`happy`,`sad`,`surprise`,`neutral`) values 
(1,3,'2023-03-14',NULL,'0.25','0.0','0.84','0.43','2.76','2.99','92.73'),
(2,3,'2023-03-14','09:54:23','2.09','0.02','4.36','17.14','5.43','1.02','69.95'),
(3,3,'2023-03-14','10:12:25','0.24','0.0','2.16','29.01','0.98','0.59','67.02');

/*Table structure for table `employees` */

DROP TABLE IF EXISTS `employees`;

CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dob` varchar(15) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `position` varchar(100) DEFAULT NULL,
  `doj` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `employees` */

insert  into `employees`(`id`,`log_id`,`name`,`phone`,`email`,`dob`,`gender`,`address`,`position`,`doj`) values 
(1,3,'Zayan Shamsudheen','8129777489','zs','2001-08-13','male','tgi','hr','2023-03-13');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(3,'zs','zs','employee');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
