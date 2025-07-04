USE lms_db;
SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT;
SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS;
SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION;
SET NAMES utf8mb4;
SET @OLD_TIME_ZONE=@@TIME_ZONE;
SET TIME_ZONE='+00:00';
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO';
SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0;

DROP TABLE IF EXISTS `books`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
CREATE TABLE `books` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `year_published` year(4) DEFAULT NULL,
  `total_copies` int(11) NOT NULL DEFAULT 1,
  `available_copies` int(11) NOT NULL DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`book_id`),
  UNIQUE KEY `isbn` (`isbn`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SET character_set_client = @saved_cs_client;

LOCK TABLES `books` WRITE;
ALTER TABLE `books` DISABLE KEYS;
INSERT INTO `books` VALUES
(1,'1984','George Orwell','Secker & Warburg','9780451524935',1949,5,5,'2025-06-10 19:39:35'),
(2,'To Kill a Mockingbird','Harper Lee','J.B. Lippincott & Co.','9780061120084',1960,4,4,'2025-06-10 19:39:35'),
(3,'The Great Gatsby','F. Scott Fitzgerald','Charles Scribner\'s Sons','9780743273565',1925,4,4,'2025-06-10 19:39:35'),
(4,'The Catcher in the Rye','J.D. Salinger','Little, Brown and Company','9780316769488',1951,3,3,'2025-06-10 19:39:35'),
(5,'The Hobbit','J.R.R. Tolkien','George Allen & Unwin','9780547928227',1937,5,5,'2025-06-10 19:39:35'),
(6,'Fahrenheit 451','Ray Bradbury','Ballantine Books','9781451673319',1953,4,4,'2025-06-10 19:39:35');
ALTER TABLE `books` ENABLE KEYS;
UNLOCK TABLES;

DROP TABLE IF EXISTS `issued_books`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
CREATE TABLE `issued_books` (
  `issue_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `issue_date` date NOT NULL DEFAULT (CURRENT_DATE),
  `due_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  PRIMARY KEY (`issue_id`),
  KEY `book_id` (`book_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `issued_books_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `issued_books_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SET character_set_client = @saved_cs_client;

LOCK TABLES `issued_books` WRITE;
ALTER TABLE `issued_books` DISABLE KEYS;
INSERT INTO `issued_books` VALUES
(1,6,1,'2025-06-10','2025-06-24','2025-06-12');
ALTER TABLE `issued_books` ENABLE KEYS;
UNLOCK TABLES;

DROP TABLE IF EXISTS `members`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
CREATE TABLE `members` (
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `join_date` date DEFAULT (CURRENT_DATE),
  `status` enum('active','suspended','alumni') DEFAULT 'active',
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SET character_set_client = @saved_cs_client;

LOCK TABLES `members` WRITE;
ALTER TABLE `members` DISABLE KEYS;
INSERT INTO `members` VALUES
(1,'vishnu kumar','kumarvishun24@gmai.com','8102988587','2025-06-10','active');
ALTER TABLE `members` ENABLE KEYS;
UNLOCK TABLES;

DROP TABLE IF EXISTS `users`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('member','librarian','admin') NOT NULL DEFAULT 'member',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SET character_set_client = @saved_cs_client;

LOCK TABLES `users` WRITE;
ALTER TABLE `users` DISABLE KEYS;
INSERT INTO `users` VALUES
(1,1,'vishnu-iitp','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2','member','2025-06-10 19:40:13');
ALTER TABLE `users` ENABLE KEYS;
UNLOCK TABLES;

SET TIME_ZONE=@OLD_TIME_ZONE;
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET SQL_NOTES=@OLD_SQL_NOTES;
