-- MySQL dump 10.13  Distrib 9.1.0, for macos14 (arm64)
--
-- Host: localhost    Database: RideShare
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `DRIVER`
--

DROP TABLE IF EXISTS `DRIVER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DRIVER` (
  `driver_ID` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `average_rating` int DEFAULT NULL,
  `driving_status` tinyint(1) DEFAULT '0',
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`driver_ID`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DRIVER`
--

LOCK TABLES `DRIVER` WRITE;
/*!40000 ALTER TABLE `DRIVER` DISABLE KEYS */;
INSERT INTO `DRIVER` VALUES (19280,'henryS','Chapman',6,1,'Henry S.'),(20102,'alex','Chapman',0,0,'A-Fomina'),(44888,'aGoad','Chapman',0,0,'Andrew Goad');
/*!40000 ALTER TABLE `DRIVER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RIDE`
--

DROP TABLE IF EXISTS `RIDE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RIDE` (
  `ride_ID` int NOT NULL,
  `rating` int DEFAULT NULL,
  `pickup_location` varchar(60) DEFAULT NULL,
  `drop_off_location` varchar(60) DEFAULT NULL,
  `time_stamp` timestamp NULL DEFAULT NULL,
  `driver_id` int DEFAULT NULL,
  `rider_id` int DEFAULT NULL,
  PRIMARY KEY (`ride_ID`),
  KEY `driver_id` (`driver_id`),
  KEY `rider_id` (`rider_id`),
  CONSTRAINT `ride_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `DRIVER` (`driver_ID`),
  CONSTRAINT `ride_ibfk_2` FOREIGN KEY (`rider_id`) REFERENCES `RIDER` (`rider_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RIDE`
--

LOCK TABLES `RIDE` WRITE;
/*!40000 ALTER TABLE `RIDE` DISABLE KEYS */;
INSERT INTO `RIDE` VALUES (34504,8,'CVS','Target','2024-11-07 21:25:14',19280,46286),(43915,8,'Target','IVC','2024-11-07 22:02:46',19280,14132),(44485,4,'Dodge','Keck','2024-11-07 20:37:20',19280,14132),(49067,2,'Henry\'s house','Chapman','2024-11-07 21:32:05',19280,46286),(53878,10,'Bank','School','2024-11-07 21:52:36',19280,14132);
/*!40000 ALTER TABLE `RIDE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RIDER`
--

DROP TABLE IF EXISTS `RIDER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RIDER` (
  `rider_ID` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`rider_ID`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RIDER`
--

LOCK TABLES `RIDER` WRITE;
/*!40000 ALTER TABLE `RIDER` DISABLE KEYS */;
INSERT INTO `RIDER` VALUES (5965,'','',''),(14132,'alexF','Chapman','Alexandra Fomina'),(46286,'steve','steve','steve'),(55072,'henryS','Chapman','Henry');
/*!40000 ALTER TABLE `RIDER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-07 18:05:54
