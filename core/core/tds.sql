/*
SQLyog Ultimate v9.10 
MySQL - 5.0.67-community-nt : Database - task_distribution_system
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`taskdistributionsystem` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `taskdistributionsystem`;

/*Table structure for table `client` */

DROP TABLE IF EXISTS `client`;

CREATE TABLE `client` (
  `clientId` int(11) NOT NULL auto_increment,
  `hostName` varchar(45) NOT NULL,
  `userName` varchar(45) NOT NULL,
  PRIMARY KEY  (`clientId`),
  UNIQUE KEY `clientId_UNIQUE` (`clientId`)
) ENGINE=InnoDB AUTO_INCREMENT=713 DEFAULT CHARSET=latin1;

/*Data for the table `client` */

insert  into `client`(`clientId`,`hostName`,`userName`) values (632,'TestHost','Testuser');

/*Table structure for table `node` */

DROP TABLE IF EXISTS `node`;

CREATE TABLE `node` (
  `nodeId` int(11) NOT NULL auto_increment,
  `nodeIp` varchar(50) NOT NULL,
  `nodePort` int(11) NOT NULL,
  `nodeStatus` enum('AVAILABLE','BUSY','NOT_OPERATIONAL') NOT NULL,
  PRIMARY KEY  (`nodeId`),
  UNIQUE KEY `nodeId_UNIQUE` (`nodeId`),
--  UNIQUE KEY `nodeIp_UNIQUE` (`nodeIp`)
) ENGINE=InnoDB AUTO_INCREMENT=402 DEFAULT CHARSET=latin1;

/*Data for the table `node` */


insert  into `node`(`nodeId`,`nodeIp`,`nodePort`,`nodeStatus`) values (284,'111.11.11.117',1111,'AVAILABLE');

/*Table structure for table `task` */

DROP TABLE IF EXISTS `task`;

CREATE TABLE `task` (
  `taskId` int(11) NOT NULL auto_increment,
  `taskName` varchar(45) NOT NULL,
  `taskParameter` varchar(40) default NULL,
  `taskPath` varchar(100) NOT NULL,
  `taskState` enum('PENDING','IN_PROGRESS','COMPLETED') NOT NULL,
  `userID` int(11) NOT NULL,
  `assignedNodeId` int(11) default NULL,
  PRIMARY KEY  (`taskId`),
  UNIQUE KEY `taskId_UNIQUE` (`taskId`),
  KEY `clientId_idx` (`userID`),
  KEY `nodeId_idx` (`assignedNodeId`),
  CONSTRAINT `clientId` FOREIGN KEY (`userID`) REFERENCES `client` (`clientId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `nodeId` FOREIGN KEY (`assignedNodeId`) REFERENCES `node` (`nodeId`)
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=latin1;

/*Data for the table `task` */

insert  into `task`(`taskId`,`taskName`,`taskParameter`,`taskPath`,`taskState`,`userID`,`assignedNodeId`) values (220,'testTask','x,y,z','C://task/ww','IN_PROGRESS',372,NULL);
insert  into `task`(`taskId`,`taskName`,`taskParameter`,`taskPath`,`taskState`,`userID`,`assignedNodeId`) values (250,'testTask','x,y,z','C://task/ww','IN_PROGRESS',446,NULL);

/*Table structure for table `taskresult` */

DROP TABLE IF EXISTS `taskresult`;

CREATE TABLE `taskresult` (
  `resultId` int(11) NOT NULL auto_increment,
  `taskId` int(11) NOT NULL,
  `Outcome` enum('SUCCESS','FAILED') NOT NULL,
  `ErrorCode` int(11) default NULL,
  `ErrorMsg` varchar(100) default NULL,
  `ResultBuffer` mediumblob,
  PRIMARY KEY  (`resultId`),
  KEY `taskIdKey` (`taskId`),
  CONSTRAINT `taskIdKey` FOREIGN KEY (`taskId`) REFERENCES `task` (`taskId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `taskresult` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
