-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: student_exam_system
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `exam`
--

DROP TABLE IF EXISTS `exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam` (
  `exam_id` int NOT NULL AUTO_INCREMENT,
  `exam_date` date DEFAULT NULL,
  `semester_id` int DEFAULT NULL,
  PRIMARY KEY (`exam_id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `exam_ibfk_1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam`
--

LOCK TABLES `exam` WRITE;
/*!40000 ALTER TABLE `exam` DISABLE KEYS */;
INSERT INTO `exam` VALUES (1,'2024-08-02',2),(2,'2024-05-12',2),(3,'2024-09-30',1),(4,'2023-12-31',2),(5,'2024-05-22',2),(6,'2024-08-31',1),(7,'2024-01-14',1),(8,'2024-10-11',2),(9,'2024-05-27',1),(10,'2024-11-11',1),(11,'2024-08-24',1),(12,'2024-03-27',1),(13,'2024-02-27',2),(14,'2024-06-12',2),(15,'2024-10-20',2),(16,'2024-06-05',1),(17,'2024-03-05',1),(18,'2024-06-29',1),(19,'2024-05-01',1),(20,'2024-07-20',2),(21,'2024-04-07',1),(22,'2024-03-25',1),(23,'2024-07-11',2),(24,'2024-08-07',2),(25,'2024-10-23',2);
/*!40000 ALTER TABLE `exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_result`
--

DROP TABLE IF EXISTS `exam_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_result` (
  `result_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `exam_id` int DEFAULT NULL,
  `grade` varchar(5) DEFAULT NULL,
  `category_code` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`result_id`),
  KEY `student_id` (`student_id`),
  KEY `exam_id` (`exam_id`),
  KEY `category_code` (`category_code`),
  CONSTRAINT `exam_result_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `exam_result_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exam` (`exam_id`),
  CONSTRAINT `exam_result_ibfk_3` FOREIGN KEY (`category_code`) REFERENCES `result_category` (`category_code`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_result`
--

LOCK TABLES `exam_result` WRITE;
/*!40000 ALTER TABLE `exam_result` DISABLE KEYS */;
INSERT INTO `exam_result` VALUES (1,13,9,'B','B'),(2,20,20,'A','A'),(3,4,4,'B','B'),(4,2,17,'D','D'),(5,20,19,'D','D'),(6,7,2,'F','F'),(7,6,20,'F','F'),(8,9,20,'F','F'),(9,11,8,'C','C'),(10,10,3,'A','A'),(11,21,23,'F','F'),(12,6,5,'A','A'),(13,2,6,'A','A'),(14,1,23,'A','A'),(15,2,6,'B','B'),(16,6,4,'B','B'),(17,16,18,'A','A'),(18,8,23,'C','C'),(19,18,12,'B','B'),(20,3,20,'D','D'),(21,23,7,'F','F'),(22,8,22,'D','D'),(23,15,8,'A','A'),(24,15,10,'C','C'),(25,23,5,'B','B');
/*!40000 ALTER TABLE `exam_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result_category`
--

DROP TABLE IF EXISTS `result_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `result_category` (
  `category_code` varchar(10) NOT NULL,
  `mark_low` int DEFAULT NULL,
  `mark_high` int DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`category_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result_category`
--

LOCK TABLES `result_category` WRITE;
/*!40000 ALTER TABLE `result_category` DISABLE KEYS */;
INSERT INTO `result_category` VALUES ('A',90,100,'Excellent'),('B',80,89,'Good'),('C',70,79,'Average'),('D',60,69,'Below Average'),('F',0,59,'Fail');
/*!40000 ALTER TABLE `result_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `semester_id` int NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(50) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`semester_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'1st Semester','2024-08-12','2024-12-17'),(2,'2nd Semester','2025-01-13','2025-05-23');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `sex` tinyint DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Anthony','Martin',1,'nstanley@example.com'),(2,'Tiffany','Vasquez',0,'micheletaylor@example.org'),(3,'Ashley','Reid',1,'wilsonsteve@example.org'),(4,'Lisa','Ryan',1,'russellraymond@example.com'),(5,'Alexandria','Ortiz',1,'yenglish@example.net'),(6,'Kevin','Shepard',0,'laurie99@example.net'),(7,'Willie','Hernandez',1,'robertsvictoria@example.com'),(8,'Maria','Dyer',0,'rhondadunn@example.com'),(9,'Willie','Johnson',1,'robinsoncrystal@example.net'),(10,'Joseph','Brown',1,'vmccormick@example.com'),(11,'Kristin','Cooper',0,'michaelpope@example.com'),(12,'Jerry','Ferguson',1,'jose61@example.com'),(13,'Donald','Ramirez',1,'margaretrice@example.org'),(14,'Jennifer','Rice',0,'blake21@example.org'),(15,'James','Johnson',0,'johnrobles@example.com'),(16,'Richard','Peterson',1,'monicastrickland@example.net'),(17,'Gregory','Roberts',1,'heathermarshall@example.net'),(18,'Patrick','Strong',1,'rodriguezdavid@example.org'),(19,'Stephen','Taylor',0,'elucero@example.com'),(20,'Angela','Sims',1,'gonzalezjames@example.com'),(21,'Richard','Pollard',1,'bettydixon@example.com'),(22,'Anita','Sanchez',0,'darlene57@example.net'),(23,'Teresa','Johnson',1,'coffeypatricia@example.net'),(24,'Brittany','Holt',1,'trevorrios@example.net'),(25,'Sandra','Allen',0,'mary16@example.com');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-10 13:55:37
