-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: starstore
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `discount_codes`
--

DROP TABLE IF EXISTS `discount_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discount_codes` (
  `discountID` int NOT NULL AUTO_INCREMENT,
  `DiscountCode` varchar(45) NOT NULL,
  `Used` int NOT NULL,
  `expiryDate` date DEFAULT NULL,
  `discountPercentage` float DEFAULT NULL,
  PRIMARY KEY (`discountID`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount_codes`
--

LOCK TABLES `discount_codes` WRITE;
/*!40000 ALTER TABLE `discount_codes` DISABLE KEYS */;
INSERT INTO `discount_codes` VALUES (2,'CODE1001',0,'2024-12-31',10),(4,'CODE1003',0,'2020-11-15',20),(5,'CODE1004',0,'2023-01-01',5),(6,'CODE1005',1,'2024-07-22',25),(7,'CODE1006',0,'2025-08-09',18),(8,'CODE1007',0,'2021-10-10',10),(9,'CODE1008',0,'2025-09-05',30),(10,'CODE1009',0,'2022-02-20',12),(11,'CODE1010',0,'2024-12-25',15),(12,'CODE1011',0,'2025-05-15',20),(13,'CODE1012',0,'2020-04-30',22),(14,'CODE1013',0,'2024-08-15',10),(15,'CODE1014',0,'2021-07-08',25),(16,'CODE1015',0,'2022-03-01',30),(17,'CODE1016',0,'2023-05-20',15),(18,'CODE1017',0,'2022-11-22',18),(19,'CODE1018',0,'2018-12-20',20),(20,'CODE1019',0,'2024-06-05',12),(21,'CODE1020',0,'2024-01-15',10),(22,'CODE1021',0,'2023-09-30',15),(23,'CODE1022',0,'2020-03-31',25),(24,'CODE1023',0,'2019-10-20',17),(25,'CODE1024',0,'2024-08-31',13),(26,'CODE1025',0,'2021-02-28',20);
/*!40000 ALTER TABLE `discount_codes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-02 11:25:18
