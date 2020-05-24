-- MySQL dump 10.17  Distrib 10.3.17-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: aquastats
-- ------------------------------------------------------
-- Server version	10.3.17-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Meetwaarden`
--

DROP TABLE IF EXISTS `Meetwaarden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Meetwaarden` (
  `MeetingID` int(11) NOT NULL AUTO_INCREMENT,
  `Datum` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Waarde` varchar(45) DEFAULT NULL,
  `PompID` int(11) DEFAULT NULL,
  `SensorID` int(11) DEFAULT NULL,
  PRIMARY KEY (`MeetingID`),
  KEY `fk_Meetwaarden_Pomp_idx` (`PompID`),
  KEY `fk_Meetwaarden_Sensor1_idx` (`SensorID`),
  CONSTRAINT `fk_Meetwaarden_Pomp` FOREIGN KEY (`PompID`) REFERENCES `Pomp` (`PompID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Meetwaarden_Sensor1` FOREIGN KEY (`SensorID`) REFERENCES `Sensor` (`SensorID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Meetwaarden`
--

LOCK TABLES `Meetwaarden` WRITE;
/*!40000 ALTER TABLE `Meetwaarden` DISABLE KEYS */;
INSERT INTO `Meetwaarden` VALUES (2,'2020-05-22 09:46:43','1.0012',NULL,1),(3,'2020-05-22 09:47:33',NULL,1,NULL),(4,'2020-05-24 14:18:49','317.1',NULL,1),(5,'2020-05-24 14:18:49','1.104',NULL,2),(6,'2020-05-24 14:18:49','23.625',NULL,3),(7,'2020-05-24 14:19:07','317.3',NULL,1),(8,'2020-05-24 14:19:07','1.104',NULL,2),(9,'2020-05-24 14:19:07','23.562',NULL,3),(10,'2020-05-24 14:52:39','290.9',NULL,1),(11,'2020-05-24 14:52:39','1.115',NULL,2),(12,'2020-05-24 14:52:39','24.937',NULL,3),(13,'2020-05-24 14:53:04','292.4',NULL,1),(14,'2020-05-24 14:53:04','1.115',NULL,2),(15,'2020-05-24 14:53:04','25.0',NULL,3),(16,'2020-05-24 14:53:34','293.4',NULL,1),(17,'2020-05-24 14:53:34','1.117',NULL,2),(18,'2020-05-24 14:53:34','25.0',NULL,3),(19,'2020-05-24 14:53:34','1',1,NULL),(20,'2020-05-24 14:53:45','293.9',NULL,1),(21,'2020-05-24 14:53:45','1.115',NULL,2),(22,'2020-05-24 14:53:45','25.062',NULL,3),(23,'2020-05-24 14:53:45','1',1,NULL),(24,'2020-05-24 14:53:56','294.2',NULL,1),(25,'2020-05-24 14:53:56','1.116',NULL,2),(26,'2020-05-24 14:53:56','25.062',NULL,3),(27,'2020-05-24 14:53:56','1',1,NULL),(28,'2020-05-24 14:54:08','294.6',NULL,1),(29,'2020-05-24 14:54:08','1.112',NULL,2),(30,'2020-05-24 14:54:08','25.125',NULL,3),(31,'2020-05-24 14:54:08','1',1,NULL),(32,'2020-05-24 14:54:19','294.9',NULL,1),(33,'2020-05-24 14:54:19','1.114',NULL,2),(34,'2020-05-24 14:54:19','25.125',NULL,3),(35,'2020-05-24 14:54:19','1',1,NULL),(36,'2020-05-24 14:54:30','295.1',NULL,1),(37,'2020-05-24 14:54:30','1.111',NULL,2),(38,'2020-05-24 14:54:30','25.125',NULL,3),(39,'2020-05-24 14:54:30','1',1,NULL),(40,'2020-05-24 14:54:41','295.5',NULL,1),(41,'2020-05-24 14:54:41','1.112',NULL,2),(42,'2020-05-24 14:54:41','25.125',NULL,3),(43,'2020-05-24 14:54:41','1',1,NULL),(44,'2020-05-24 14:54:52','295.9',NULL,1),(45,'2020-05-24 14:54:52','1.114',NULL,2),(46,'2020-05-24 14:54:52','25.187',NULL,3),(47,'2020-05-24 14:54:52','1',1,NULL),(48,'2020-05-24 14:55:04','296.2',NULL,1),(49,'2020-05-24 14:55:04','1.117',NULL,2),(50,'2020-05-24 14:55:04','25.187',NULL,3),(51,'2020-05-24 14:55:04','1',1,NULL),(52,'2020-05-24 14:55:15','296.4',NULL,1);
/*!40000 ALTER TABLE `Meetwaarden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pomp`
--

DROP TABLE IF EXISTS `Pomp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pomp` (
  `PompID` int(11) NOT NULL AUTO_INCREMENT,
  `Status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`PompID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pomp`
--

LOCK TABLES `Pomp` WRITE;
/*!40000 ALTER TABLE `Pomp` DISABLE KEYS */;
INSERT INTO `Pomp` VALUES (1,0);
/*!40000 ALTER TABLE `Pomp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sensor`
--

DROP TABLE IF EXISTS `Sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sensor` (
  `SensorID` int(11) NOT NULL AUTO_INCREMENT,
  `Eenheid` varchar(45) NOT NULL,
  `Beschrijving` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SensorID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sensor`
--

LOCK TABLES `Sensor` WRITE;
/*!40000 ALTER TABLE `Sensor` DISABLE KEYS */;
INSERT INTO `Sensor` VALUES (1,'Ph','leest zuurtegraad'),(2,'ORP','leest oxidering van een vloeistof'),(3,'Graden','Temperatuur');
/*!40000 ALTER TABLE `Sensor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-24 17:02:37
