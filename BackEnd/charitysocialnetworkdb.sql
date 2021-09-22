-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: charitysocialnetworkdb
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `appcharitysocialnetwork_auctionitem`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_auctionitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_auctionitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `price_start` decimal(50,2) NOT NULL,
  `price_received` decimal(50,2) NOT NULL,
  `receiver_id` bigint DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `post_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork_auctionitem_post_id_1a8f1f23_uniq` (`post_id`),
  KEY `AppCharitySocialNetw_receiver_id_bbe74028_fk_AppCharit` (`receiver_id`),
  KEY `AppCharitySocialNetwork_auctionitem_post_id_1a8f1f23` (`post_id`),
  CONSTRAINT `AppCharitySocialNetw_post_id_1a8f1f23_fk_AppCharit` FOREIGN KEY (`post_id`) REFERENCES `appcharitysocialnetwork_newspost` (`id`),
  CONSTRAINT `AppCharitySocialNetw_receiver_id_bbe74028_fk_AppCharit` FOREIGN KEY (`receiver_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_auctionitem`
--

LOCK TABLES `appcharitysocialnetwork_auctionitem` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_auctionitem` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_auctionitem` VALUES (1,'Xe đạp','','','2021-07-31 09:56:55.632666','2021-07-31 09:58:14.900336',1000000.00,0.00,NULL,1,3);
/*!40000 ALTER TABLE `appcharitysocialnetwork_auctionitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_comment`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `content` longtext NOT NULL,
  `comment_parent_id` bigint DEFAULT NULL,
  `newspost_id` bigint NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppCharitySocialNetw_comment_parent_id_963c59ff_fk_AppCharit` (`comment_parent_id`),
  KEY `AppCharitySocialNetw_newspost_id_2fa82bd7_fk_AppCharit` (`newspost_id`),
  KEY `AppCharitySocialNetw_user_id_726f0c42_fk_AppCharit` (`user_id`),
  CONSTRAINT `AppCharitySocialNetw_comment_parent_id_963c59ff_fk_AppCharit` FOREIGN KEY (`comment_parent_id`) REFERENCES `appcharitysocialnetwork_comment` (`id`),
  CONSTRAINT `AppCharitySocialNetw_newspost_id_2fa82bd7_fk_AppCharit` FOREIGN KEY (`newspost_id`) REFERENCES `appcharitysocialnetwork_newspost` (`id`),
  CONSTRAINT `AppCharitySocialNetw_user_id_726f0c42_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_comment`
--

LOCK TABLES `appcharitysocialnetwork_comment` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_comment` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_comment` VALUES (1,'2021-07-31 09:52:53.374427','2021-07-31 09:52:53.374427','hay quá',NULL,1,3,1),(2,'2021-07-31 09:53:14.777022','2021-07-31 09:53:14.777022','sắp đc lên chức',1,1,3,1),(3,'2021-07-31 09:53:34.264445','2021-07-31 09:53:34.264445','ờ ha',1,1,1,1),(4,'2021-07-31 09:53:45.095676','2021-07-31 09:53:45.095676','pùn',NULL,2,3,1);
/*!40000 ALTER TABLE `appcharitysocialnetwork_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_emotioncomment`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_emotioncomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_emotioncomment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `author_id` bigint NOT NULL,
  `comment_id` bigint NOT NULL,
  `emotion_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork__author_id_comment_id_ef065011_uniq` (`author_id`,`comment_id`),
  KEY `AppCharitySocialNetw_comment_id_d4e9e0ee_fk_AppCharit` (`comment_id`),
  KEY `AppCharitySocialNetw_emotion_type_id_af47efa0_fk_AppCharit` (`emotion_type_id`),
  CONSTRAINT `AppCharitySocialNetw_author_id_18d3ceb8_fk_AppCharit` FOREIGN KEY (`author_id`) REFERENCES `appcharitysocialnetwork_user` (`id`),
  CONSTRAINT `AppCharitySocialNetw_comment_id_d4e9e0ee_fk_AppCharit` FOREIGN KEY (`comment_id`) REFERENCES `appcharitysocialnetwork_comment` (`id`),
  CONSTRAINT `AppCharitySocialNetw_emotion_type_id_af47efa0_fk_AppCharit` FOREIGN KEY (`emotion_type_id`) REFERENCES `appcharitysocialnetwork_emotiontype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_emotioncomment`
--

LOCK TABLES `appcharitysocialnetwork_emotioncomment` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_emotioncomment` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_emotioncomment` VALUES (1,'2021-07-31 09:56:03.931770','2021-07-31 09:56:03.931770',1,1,1,1),(2,'2021-07-31 09:56:13.405462','2021-07-31 09:56:13.405462',1,1,2,1),(3,'2021-07-31 09:56:18.957467','2021-07-31 09:56:18.957467',1,2,3,1),(4,'2021-07-31 09:56:24.689074','2021-07-31 09:56:24.689074',1,2,4,5);
/*!40000 ALTER TABLE `appcharitysocialnetwork_emotioncomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_emotionpost`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_emotionpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_emotionpost` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `author_id` bigint NOT NULL,
  `emotion_type_id` bigint DEFAULT NULL,
  `post_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork__author_id_post_id_4f3fdf5c_uniq` (`author_id`,`post_id`),
  KEY `AppCharitySocialNetw_emotion_type_id_bec8e2d0_fk_AppCharit` (`emotion_type_id`),
  KEY `AppCharitySocialNetw_post_id_c00a5f9a_fk_AppCharit` (`post_id`),
  CONSTRAINT `AppCharitySocialNetw_author_id_b669f430_fk_AppCharit` FOREIGN KEY (`author_id`) REFERENCES `appcharitysocialnetwork_user` (`id`),
  CONSTRAINT `AppCharitySocialNetw_emotion_type_id_bec8e2d0_fk_AppCharit` FOREIGN KEY (`emotion_type_id`) REFERENCES `appcharitysocialnetwork_emotiontype` (`id`),
  CONSTRAINT `AppCharitySocialNetw_post_id_c00a5f9a_fk_AppCharit` FOREIGN KEY (`post_id`) REFERENCES `appcharitysocialnetwork_newspost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_emotionpost`
--

LOCK TABLES `appcharitysocialnetwork_emotionpost` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_emotionpost` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_emotionpost` VALUES (1,'2021-07-31 09:55:02.320623','2021-07-31 09:55:02.320623',1,1,1,1),(2,'2021-07-31 09:55:17.880442','2021-07-31 09:55:17.880442',1,2,3,1),(3,'2021-07-31 09:55:32.749157','2021-07-31 09:55:32.749157',1,2,4,2),(4,'2021-07-31 09:55:42.049199','2021-07-31 09:55:42.049199',1,3,4,2);
/*!40000 ALTER TABLE `appcharitysocialnetwork_emotionpost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_emotiontype`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_emotiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_emotiontype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_emotiontype`
--

LOCK TABLES `appcharitysocialnetwork_emotiontype` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_emotiontype` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_emotiontype` VALUES (1,'','','2021-07-31 09:54:03.586618','2021-07-31 09:54:03.586618',1,'Like'),(2,'','','2021-07-31 09:54:08.251402','2021-07-31 09:54:08.251402',1,'Love'),(3,'','','2021-07-31 09:54:12.617451','2021-07-31 09:54:12.617451',1,'Sad'),(4,'','','2021-07-31 09:54:17.547795','2021-07-31 09:54:17.547795',1,'Wow'),(5,'','','2021-07-31 09:54:26.840039','2021-07-31 09:54:26.840039',1,'Care'),(6,'','','2021-07-31 09:54:43.713695','2021-07-31 09:54:43.713695',1,'Haha'),(7,'','','2021-07-31 09:54:52.015710','2021-07-31 09:54:52.015710',1,'Angry');
/*!40000 ALTER TABLE `appcharitysocialnetwork_emotiontype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_hashtag`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_hashtag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork_hashtag_name_74fc3822_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_hashtag`
--

LOCK TABLES `appcharitysocialnetwork_hashtag` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_hashtag` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_hashtag` VALUES (1,'Trẻ em','','2021-07-31 04:40:23.180354','2021-07-31 04:40:23.180354',1),(2,'Đấu giá','','2021-07-31 09:58:00.429477','2021-07-31 09:58:00.429477',1);
/*!40000 ALTER TABLE `appcharitysocialnetwork_hashtag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_historyauction`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_historyauction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_historyauction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `price` decimal(50,2) NOT NULL,
  `post_id` bigint NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `AppCharitySocialNetw_post_id_f750d498_fk_AppCharit` (`post_id`),
  KEY `AppCharitySocialNetw_user_id_677f009c_fk_AppCharit` (`user_id`),
  CONSTRAINT `AppCharitySocialNetw_post_id_f750d498_fk_AppCharit` FOREIGN KEY (`post_id`) REFERENCES `appcharitysocialnetwork_newspost` (`id`),
  CONSTRAINT `AppCharitySocialNetw_user_id_677f009c_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_historyauction`
--

LOCK TABLES `appcharitysocialnetwork_historyauction` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_historyauction` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_historyauction` VALUES (1,'','2021-07-31 10:04:00.455637','2021-07-31 10:04:00.455637',1,123123123.00,3,3),(2,'','2021-07-31 10:04:11.298372','2021-07-31 10:04:11.298372',1,2323.00,3,2);
/*!40000 ALTER TABLE `appcharitysocialnetwork_historyauction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_newscategory`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_newscategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_newscategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork_newscategory_name_c21a71bb_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_newscategory`
--

LOCK TABLES `appcharitysocialnetwork_newscategory` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_newscategory` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_newscategory` VALUES (1,'Quỹ bảo trợ trẻ em Việt Nam','','','2021-07-31 04:39:52.572768','2021-07-31 04:39:52.572768',1),(2,'Tổ chức trẻ em Rồng Xanh','','','2021-07-31 09:51:38.664724','2021-07-31 09:51:38.664724',1),(3,'Làng Trẻ em SOS Việt Nam.','','','2021-07-31 09:51:48.981669','2021-07-31 09:51:48.981669',1),(4,'Đấu giá','','','2021-07-31 09:57:53.410742','2021-07-31 09:57:53.410742',1);
/*!40000 ALTER TABLE `appcharitysocialnetwork_newscategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_newspost`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_newspost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_newspost` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `content` longtext NOT NULL,
  `category_id` bigint DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork_newspost_title_a56aa7cb_uniq` (`title`),
  KEY `AppCharitySocialNetw_user_id_27b8c58e_fk_AppCharit` (`user_id`),
  KEY `AppCharitySocialNetw_category_id_621d2765_fk_AppCharit` (`category_id`),
  CONSTRAINT `AppCharitySocialNetw_category_id_621d2765_fk_AppCharit` FOREIGN KEY (`category_id`) REFERENCES `appcharitysocialnetwork_newscategory` (`id`),
  CONSTRAINT `AppCharitySocialNetw_user_id_27b8c58e_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_newspost`
--

LOCK TABLES `appcharitysocialnetwork_newspost` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_newspost` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_newspost` VALUES (1,'Đây là khu vực tập trung nhiều khu nhà trọ công nhân đang rất khó khăn. Khi khảo sát nhu cầu, thật thương khi bà con cho biết cần nhất lúc này là gạo và mì gói. Với 10kg gạo mỗi phần quà, riêng khu vực phường Tân Tạo A, Quỹ Bông Sen đã chuyển đến tận tay','images/appcharitysocialnetwork_auctionitem.png','sdf','2021-07-31 04:40:25.237577','2021-07-31 04:40:25.237577','asdf',1,2,1),(2,'400 TRIỆU ĐỒNG CHO TRẺ EM ẢNH HƯỞNG COVID -19 TẠI TỈNH HÀ GIANG VÀ TUYÊN QUANG','','','2021-07-31 09:52:21.211602','2021-07-31 09:52:21.211602','qưerqwer',2,2,1),(3,'Đấu giá chiếc xe đạp','','','2021-07-31 09:58:02.502746','2021-07-31 09:58:02.503773','Đấu giá',4,2,1);
/*!40000 ALTER TABLE `appcharitysocialnetwork_newspost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_newspost_hashtag`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_newspost_hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_newspost_hashtag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `newspost_id` bigint NOT NULL,
  `hashtag_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork__newspost_id_hashtag_id_c91c180c_uniq` (`newspost_id`,`hashtag_id`),
  KEY `AppCharitySocialNetw_hashtag_id_c976d630_fk_AppCharit` (`hashtag_id`),
  CONSTRAINT `AppCharitySocialNetw_hashtag_id_c976d630_fk_AppCharit` FOREIGN KEY (`hashtag_id`) REFERENCES `appcharitysocialnetwork_hashtag` (`id`),
  CONSTRAINT `AppCharitySocialNetw_newspost_id_e520d699_fk_AppCharit` FOREIGN KEY (`newspost_id`) REFERENCES `appcharitysocialnetwork_newspost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_newspost_hashtag`
--

LOCK TABLES `appcharitysocialnetwork_newspost_hashtag` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_newspost_hashtag` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_newspost_hashtag` VALUES (1,1,1),(2,2,1),(3,3,2);
/*!40000 ALTER TABLE `appcharitysocialnetwork_newspost_hashtag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_optionreport`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_optionreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_optionreport` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_optionreport`
--

LOCK TABLES `appcharitysocialnetwork_optionreport` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_optionreport` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_optionreport` VALUES (1,'Thô tục'),(2,'Chưa chuyển tiền');
/*!40000 ALTER TABLE `appcharitysocialnetwork_optionreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_report`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `content` longtext NOT NULL,
  `reason_id` bigint DEFAULT NULL,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `active` tinyint(1) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `AppCharitySocialNetw_post_id_0b2a8e8e_fk_AppCharit` (`post_id`),
  KEY `AppCharitySocialNetw_user_id_c316def4_fk_AppCharit` (`user_id`),
  KEY `AppCharitySocialNetwork_report_reason_id_98150144` (`reason_id`),
  CONSTRAINT `AppCharitySocialNetw_post_id_0b2a8e8e_fk_AppCharit` FOREIGN KEY (`post_id`) REFERENCES `appcharitysocialnetwork_newspost` (`id`),
  CONSTRAINT `AppCharitySocialNetw_reason_id_98150144_fk_AppCharit` FOREIGN KEY (`reason_id`) REFERENCES `appcharitysocialnetwork_optionreport` (`id`),
  CONSTRAINT `AppCharitySocialNetw_user_id_c316def4_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_report`
--

LOCK TABLES `appcharitysocialnetwork_report` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_report` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_report` VALUES (1,'2021-07-31 10:02:44.242029','2021-07-31 10:02:44.242029','này chưa thanh toán viện phí',2,3,2,1,''),(2,'2021-07-31 10:03:27.616666','2021-07-31 10:03:27.616666','thằng này sử dụng tuwqf nghữ thô bạo',1,1,3,1,'');
/*!40000 ALTER TABLE `appcharitysocialnetwork_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_transaction`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_transaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `amount` int NOT NULL,
  `message` longtext NOT NULL,
  `provider_id` bigint DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `order_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `AppCharitySocialNetw_provider_id_e40ff878_fk_AppCharit` (`provider_id`),
  CONSTRAINT `AppCharitySocialNetw_provider_id_e40ff878_fk_AppCharit` FOREIGN KEY (`provider_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_transaction`
--

LOCK TABLES `appcharitysocialnetwork_transaction` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_transaction` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_transaction` VALUES (1,'','','2021-07-31 10:04:52.677071','2021-07-31 10:04:52.677071',100000,'ok',2,1,'1212222');
/*!40000 ALTER TABLE `appcharitysocialnetwork_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_user`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `nick_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_user`
--

LOCK TABLES `appcharitysocialnetwork_user` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_user` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_user` VALUES (1,'pbkdf2_sha256$260000$pnmQjtCrBCAtQ6QUOedPnR$X2avySso3nr76OMSmDk/LMEK6ZdDv0Lgnq6CrIJlKWw=','2021-07-31 02:32:40.636000',1,'admin','','','admin@s.com',1,1,'2021-07-31 02:32:29.015000',NULL,'',NULL,'0',NULL,NULL),(2,'pbkdf2_sha256$260000$EmCQCBnqkxIdNsPmwXpKsD$0kdE8wYvegcedtB+D5pZVbewJRDtSD+pZN/b4sw1Z7Y=',NULL,0,'tandat','Tấn','Đạt','vutandat29092000@gmail.com',0,1,'2021-07-31 03:45:11.000000',NULL,'',NULL,'man',NULL,'0965929852'),(3,'pbkdf2_sha256$260000$4TzarGeOJ6VpOjU4eXxTeg$vn0cGg239Tc9fcmu/7+fwkV+Md7Hskej8M8eviwS7WU=',NULL,0,'usermod','user','mod','',0,1,'2021-07-31 09:49:47.000000',NULL,'',NULL,'man',NULL,'0965929852');
/*!40000 ALTER TABLE `appcharitysocialnetwork_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_user_groups`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork__user_id_group_id_f2305995_uniq` (`user_id`,`group_id`),
  KEY `AppCharitySocialNetw_group_id_b63764d2_fk_auth_grou` (`group_id`),
  CONSTRAINT `AppCharitySocialNetw_group_id_b63764d2_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `AppCharitySocialNetw_user_id_3d6e0c4b_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_user_groups`
--

LOCK TABLES `appcharitysocialnetwork_user_groups` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_user_groups` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_user_groups` VALUES (6,2,1),(1,2,2),(2,2,3),(3,2,4),(4,2,5),(5,2,6),(7,3,1),(8,3,2),(9,3,3),(10,3,4),(11,3,5),(12,3,6),(13,3,7);
/*!40000 ALTER TABLE `appcharitysocialnetwork_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appcharitysocialnetwork_user_user_permissions`
--

DROP TABLE IF EXISTS `appcharitysocialnetwork_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appcharitysocialnetwork_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppCharitySocialNetwork__user_id_permission_id_e0ef06ac_uniq` (`user_id`,`permission_id`),
  KEY `AppCharitySocialNetw_permission_id_366780db_fk_auth_perm` (`permission_id`),
  CONSTRAINT `AppCharitySocialNetw_permission_id_366780db_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `AppCharitySocialNetw_user_id_479c1bfa_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appcharitysocialnetwork_user_user_permissions`
--

LOCK TABLES `appcharitysocialnetwork_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `appcharitysocialnetwork_user_user_permissions` DISABLE KEYS */;
INSERT INTO `appcharitysocialnetwork_user_user_permissions` VALUES (1,3,73);
/*!40000 ALTER TABLE `appcharitysocialnetwork_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (6,'Auctions'),(7,'Browse Articles'),(5,'Emotion'),(4,'Hashtags'),(2,'Post'),(3,'Report'),(1,'User');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,22),(2,1,24),(45,2,29),(46,2,30),(47,2,31),(44,2,32),(50,3,37),(51,3,38),(49,3,40),(48,3,56),(53,4,61),(54,4,62),(55,4,63),(52,4,64),(62,5,52),(56,5,65),(57,5,66),(58,5,68),(59,5,69),(60,5,70),(61,5,72),(64,6,33),(65,6,34),(66,6,36),(63,6,48),(69,7,30),(67,7,32),(68,7,73);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add news category',7,'add_newscategory'),(26,'Can change news category',7,'change_newscategory'),(27,'Can delete news category',7,'delete_newscategory'),(28,'Can view news category',7,'view_newscategory'),(29,'Can add news post',8,'add_newspost'),(30,'Can change news post',8,'change_newspost'),(31,'Can delete news post',8,'delete_newspost'),(32,'Can view news post',8,'view_newspost'),(33,'Can add transaction',9,'add_transaction'),(34,'Can change transaction',9,'change_transaction'),(35,'Can delete transaction',9,'delete_transaction'),(36,'Can view transaction',9,'view_transaction'),(37,'Can add report',10,'add_report'),(38,'Can change report',10,'change_report'),(39,'Can delete report',10,'delete_report'),(40,'Can view report',10,'view_report'),(41,'Can add comment',11,'add_comment'),(42,'Can change comment',11,'change_comment'),(43,'Can delete comment',11,'delete_comment'),(44,'Can view comment',11,'view_comment'),(45,'Can add auction item',12,'add_auctionitem'),(46,'Can change auction item',12,'change_auctionitem'),(47,'Can delete auction item',12,'delete_auctionitem'),(48,'Can view auction item',12,'view_auctionitem'),(49,'Can add emotion type',13,'add_emotiontype'),(50,'Can change emotion type',13,'change_emotiontype'),(51,'Can delete emotion type',13,'delete_emotiontype'),(52,'Can view emotion type',13,'view_emotiontype'),(53,'Can add option report',14,'add_optionreport'),(54,'Can change option report',14,'change_optionreport'),(55,'Can delete option report',14,'delete_optionreport'),(56,'Can view option report',14,'view_optionreport'),(57,'Can add history auction',15,'add_historyauction'),(58,'Can change history auction',15,'change_historyauction'),(59,'Can delete history auction',15,'delete_historyauction'),(60,'Can view history auction',15,'view_historyauction'),(61,'Can add hashtag',16,'add_hashtag'),(62,'Can change hashtag',16,'change_hashtag'),(63,'Can delete hashtag',16,'delete_hashtag'),(64,'Can view hashtag',16,'view_hashtag'),(65,'Can add emotion post',17,'add_emotionpost'),(66,'Can change emotion post',17,'change_emotionpost'),(67,'Can delete emotion post',17,'delete_emotionpost'),(68,'Can view emotion post',17,'view_emotionpost'),(69,'Can add emotion comment',18,'add_emotioncomment'),(70,'Can change emotion comment',18,'change_emotioncomment'),(71,'Can delete emotion comment',18,'delete_emotioncomment'),(72,'Can view emotion comment',18,'view_emotioncomment'),(73,'Browse Articles',8,'mod');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_AppCharit` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_AppCharit` FOREIGN KEY (`user_id`) REFERENCES `appcharitysocialnetwork_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-07-31 03:44:11.130520','1','User Normal',1,'[{\"added\": {}}]',3,1),(2,'2021-07-31 03:45:11.749135','2','userpost',1,'[{\"added\": {}}]',6,1),(3,'2021-07-31 03:50:51.097005','2','Post',1,'[{\"added\": {}}]',3,1),(4,'2021-07-31 03:51:56.894278','3','Report',1,'[{\"added\": {}}]',3,1),(5,'2021-07-31 03:53:22.542681','4','Hashtags',1,'[{\"added\": {}}]',3,1),(6,'2021-07-31 03:57:01.957677','5','Emotion',1,'[{\"added\": {}}]',3,1),(7,'2021-07-31 04:00:07.317538','6','Auctions',1,'[{\"added\": {}}]',3,1),(8,'2021-07-31 04:01:35.699549','2','tandat',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\", \"Groups\", \"Phone number\", \"Gender\"]}}]',6,1),(9,'2021-07-31 04:03:17.844783','1','User Normal',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(10,'2021-07-31 04:03:22.855923','1','User',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',3,1),(11,'2021-07-31 04:03:37.727672','2','tandat',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,1),(12,'2021-07-31 04:09:31.635093','73','AppCharitySocialNetwork | news post | Browse Articles',1,'[{\"added\": {}}]',2,1),(13,'2021-07-31 04:11:40.945413','7','Browse Articles',1,'[{\"added\": {}}]',3,1),(14,'2021-07-31 04:39:52.574762','1','Quỹ bảo trợ trẻ em Việt Nam',1,'[{\"added\": {}}]',7,1),(15,'2021-07-31 04:40:23.182349','1','Trẻ em',1,'[{\"added\": {}}]',16,1),(16,'2021-07-31 04:40:25.245520','1','Đây là khu vực tập trung nhiều khu nhà trọ công nhân đang rất khó khăn. Khi khảo sát nhu cầu, thật thương khi bà con cho biết cần nhất lúc này là gạo và mì gói. Với 10kg gạo mỗi phần quà, riêng khu vự',1,'[{\"added\": {}}, {\"added\": {\"name\": \"newspost-hashtag relationship\", \"object\": \"NewsPost_hashtag object (1)\"}}]',8,1),(17,'2021-07-31 09:49:47.245790','3','usermod',1,'[{\"added\": {}}]',6,1),(18,'2021-07-31 09:50:20.410280','3','usermod',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Groups\", \"User permissions\", \"Phone number\", \"Gender\"]}}]',6,1),(19,'2021-07-31 09:51:38.665720','2','Tổ chức trẻ em Rồng Xanh',1,'[{\"added\": {}}]',7,1),(20,'2021-07-31 09:51:48.983667','3','Làng Trẻ em SOS Việt Nam.',1,'[{\"added\": {}}]',7,1),(21,'2021-07-31 09:52:21.217586','2','400 TRIỆU ĐỒNG CHO TRẺ EM ẢNH HƯỞNG COVID -19 TẠI TỈNH HÀ GIANG VÀ TUYÊN QUANG',1,'[{\"added\": {}}, {\"added\": {\"name\": \"newspost-hashtag relationship\", \"object\": \"NewsPost_hashtag object (2)\"}}]',8,1),(22,'2021-07-31 09:52:53.378415','1','hay quá',1,'[{\"added\": {}}]',11,1),(23,'2021-07-31 09:53:14.778028','2','sắp đc lên chức',1,'[{\"added\": {}}]',11,1),(24,'2021-07-31 09:53:34.266435','3','ờ ha',1,'[{\"added\": {}}]',11,1),(25,'2021-07-31 09:53:45.097672','4','pùn',1,'[{\"added\": {}}]',11,1),(26,'2021-07-31 09:54:03.587615','1','Like',1,'[{\"added\": {}}]',13,1),(27,'2021-07-31 09:54:08.252475','2','Love',1,'[{\"added\": {}}]',13,1),(28,'2021-07-31 09:54:12.618042','3','Sad',1,'[{\"added\": {}}]',13,1),(29,'2021-07-31 09:54:17.549836','4','Wow',1,'[{\"added\": {}}]',13,1),(30,'2021-07-31 09:54:26.841406','5','Care',1,'[{\"added\": {}}]',13,1),(31,'2021-07-31 09:54:43.718428','6','Haha',1,'[{\"added\": {}}]',13,1),(32,'2021-07-31 09:54:52.017109','7','Angry',1,'[{\"added\": {}}]',13,1),(33,'2021-07-31 09:55:02.323578','1','admin :  -> Like',1,'[{\"added\": {}}]',17,1),(34,'2021-07-31 09:55:17.882439','2','tandat : Tấn Đạt -> Sad',1,'[{\"added\": {}}]',17,1),(35,'2021-07-31 09:55:32.750854','3','tandat : Tấn Đạt -> Wow',1,'[{\"added\": {}}]',17,1),(36,'2021-07-31 09:55:42.051211','4','usermod : user mod -> Wow',1,'[{\"added\": {}}]',17,1),(37,'2021-07-31 09:56:03.933943','1','admin :  -> Like',1,'[{\"added\": {}}]',18,1),(38,'2021-07-31 09:56:13.406933','2','admin :  -> Like',1,'[{\"added\": {}}]',18,1),(39,'2021-07-31 09:56:18.959462','3','tandat : Tấn Đạt -> Like',1,'[{\"added\": {}}]',18,1),(40,'2021-07-31 09:56:24.693883','4','tandat : Tấn Đạt -> Care',1,'[{\"added\": {}}]',18,1),(41,'2021-07-31 09:56:55.636655','1','Xe đạp',1,'[{\"added\": {}}]',12,1),(42,'2021-07-31 09:57:17.607705','2','xe máy',1,'[{\"added\": {}}]',12,1),(43,'2021-07-31 09:57:53.412737','4','Đấu giá',1,'[{\"added\": {}}]',7,1),(44,'2021-07-31 09:58:00.430916','2','Đấu giá',1,'[{\"added\": {}}]',16,1),(45,'2021-07-31 09:58:02.511274','3','Đấu giá chiếc xe đạp',1,'[{\"added\": {}}, {\"added\": {\"name\": \"newspost-hashtag relationship\", \"object\": \"NewsPost_hashtag object (3)\"}}]',8,1),(46,'2021-07-31 09:58:14.902505','1','Xe đạp',2,'[{\"changed\": {\"fields\": [\"Post\"]}}]',12,1),(47,'2021-07-31 09:58:20.014856','2','xe máy',2,'[{\"changed\": {\"fields\": [\"Post\"]}}]',12,1),(48,'2021-07-31 09:59:35.248752','2','xe máy',3,'',12,1),(49,'2021-07-31 10:00:46.265510','3','xe máy',1,'[{\"added\": {}}]',12,1),(50,'2021-07-31 10:00:55.573080','3','xe máy',3,'',12,1),(51,'2021-07-31 10:01:14.225001','1','OptionReport object (1)',1,'[{\"added\": {}}]',14,1),(52,'2021-07-31 10:01:32.124482','2','OptionReport object (2)',1,'[{\"added\": {}}]',14,1),(53,'2021-07-31 10:02:44.246018','1','này chưa thanh toán viện phí',1,'[{\"added\": {}}]',10,1),(54,'2021-07-31 10:03:27.617663','2','thằng này sử dụng tuwqf nghữ thô bạo',1,'[{\"added\": {}}]',10,1),(55,'2021-07-31 10:04:00.458628','1','user mod : Đấu giá chiếc xe đạp -> 123123123',1,'[{\"added\": {}}]',15,1),(56,'2021-07-31 10:04:11.300367','2','Tấn Đạt : Đấu giá chiếc xe đạp -> 2323',1,'[{\"added\": {}}]',15,1),(57,'2021-07-31 10:04:52.679102','1','1212222-ok',1,'[{\"added\": {}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(12,'AppCharitySocialNetwork','auctionitem'),(11,'AppCharitySocialNetwork','comment'),(18,'AppCharitySocialNetwork','emotioncomment'),(17,'AppCharitySocialNetwork','emotionpost'),(13,'AppCharitySocialNetwork','emotiontype'),(16,'AppCharitySocialNetwork','hashtag'),(15,'AppCharitySocialNetwork','historyauction'),(7,'AppCharitySocialNetwork','newscategory'),(8,'AppCharitySocialNetwork','newspost'),(14,'AppCharitySocialNetwork','optionreport'),(10,'AppCharitySocialNetwork','report'),(9,'AppCharitySocialNetwork','transaction'),(6,'AppCharitySocialNetwork','user'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-07-31 02:58:19.354182'),(2,'contenttypes','0002_remove_content_type_name','2021-07-31 02:58:19.494765'),(3,'auth','0001_initial','2021-07-31 02:58:20.248726'),(4,'auth','0002_alter_permission_name_max_length','2021-07-31 02:58:20.342486'),(5,'auth','0003_alter_user_email_max_length','2021-07-31 02:58:20.358105'),(6,'auth','0004_alter_user_username_opts','2021-07-31 02:58:20.358105'),(7,'auth','0005_alter_user_last_login_null','2021-07-31 02:58:20.373733'),(8,'auth','0006_require_contenttypes_0002','2021-07-31 02:58:20.373733'),(9,'auth','0007_alter_validators_add_error_messages','2021-07-31 02:58:20.389319'),(10,'auth','0008_alter_user_username_max_length','2021-07-31 02:58:20.389319'),(11,'auth','0009_alter_user_last_name_max_length','2021-07-31 02:58:20.404941'),(12,'auth','0010_alter_group_name_max_length','2021-07-31 02:58:20.436183'),(13,'auth','0011_update_proxy_permissions','2021-07-31 02:58:20.436183'),(14,'auth','0012_alter_user_first_name_max_length','2021-07-31 02:58:20.451804'),(15,'AppCharitySocialNetwork','0001_initial','2021-07-31 02:58:21.170675'),(16,'AppCharitySocialNetwork','0002_auto_20210728_2250','2021-07-31 02:58:23.095253'),(17,'AppCharitySocialNetwork','0003_auto_20210730_2300','2021-07-31 02:58:28.328400'),(18,'AppCharitySocialNetwork','0004_auto_20210730_2314','2021-07-31 02:58:28.750208'),(19,'admin','0001_initial','2021-07-31 02:58:29.296921'),(20,'admin','0002_logentry_remove_auto_add','2021-07-31 02:58:29.312545'),(21,'admin','0003_logentry_add_action_flag_choices','2021-07-31 02:58:29.343821'),(22,'sessions','0001_initial','2021-07-31 02:58:29.421891'),(23,'AppCharitySocialNetwork','0005_alter_auctionitem_post','2021-07-31 09:59:46.322764'),(24,'AppCharitySocialNetwork','0006_auto_20210731_1710','2021-07-31 10:10:48.185559');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('hh7eoua013xoqye0x4anyu5p6detzeij','.eJxVjM0OwiAQhN-FsyEgP0s9evcZCMsuUjU0Ke3J-O62SQ-azGm-b-YtYlqXGtfOcxxJXIQWp98OU35y2wE9UrtPMk9tmUeUuyIP2uVtIn5dD_fvoKZetzVoJp1dwMzKGjagLJgzsEJCUsUobZ1WAw66AHoOPjhDuMURFwAvPl_bRjfP:1m9eno:nFohvcHMd0GACbXJ4qglEgVZvuP59hr5yyc5wPYxbaE','2021-08-14 02:32:40.642000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'charitysocialnetworkdb'
--

--
-- Dumping routines for database 'charitysocialnetworkdb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-31 17:16:56
