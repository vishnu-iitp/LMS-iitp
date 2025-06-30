DROP TABLE IF EXISTS `books`;

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

LOCK TABLES `books` WRITE;

INSERT INTO `books` VALUES
(1,'1984','George Orwell','Secker & Warburg','9780451524935',1949,5,5,'2025-06-10 19:39:35'),
(2,'To Kill a Mockingbird','Harper Lee','J.B. Lippincott & Co.','9780061120084',1960,4,4,'2025-06-10 19:39:35'),
(3,'The Great Gatsby','F. Scott Fitzgerald','Charles Scribner\'s Sons','9780743273565',1925,4,4,'2025-06-10 19:39:35'),
(4,'The Catcher in the Rye','J.D. Salinger','Little, Brown and Company','9780316769488',1951,3,3,'2025-06-10 19:39:35'),
(5,'The Hobbit','J.R.R. Tolkien','George Allen & Unwin','9780547928227',1937,5,5,'2025-06-10 19:39:35'),
(6,'Fahrenheit 451','Ray Bradbury','Ballantine Books','9781451673319',1953,4,4,'2025-06-10 19:39:35');

UNLOCK TABLES;

DROP TABLE IF EXISTS `issued_books`;

CREATE TABLE `issued_books` (
  `issue_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `issue_date` date NOT NULL DEFAULT curdate(),
  `due_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  PRIMARY KEY (`issue_id`),
  KEY `book_id` (`book_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `issued_books_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `issued_books_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOCK TABLES `issued_books` WRITE;

INSERT INTO `issued_books` VALUES
(1,6,1,'2025-06-10','2025-06-24','2025-06-12');

UNLOCK TABLES;

DROP TABLE IF EXISTS `members`;

CREATE TABLE `members` (
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `join_date` date DEFAULT curdate(),
  `status` enum('active','suspended','alumni') DEFAULT 'active',
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOCK TABLES `members` WRITE;

INSERT INTO `members` VALUES
(1,'vishnu kumar','kumarvis****@gmai.com','81029*****','2025-06-10','active');

UNLOCK TABLES;

DROP TABLE IF EXISTS `users`;

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

LOCK TABLES `users` WRITE;

INSERT INTO `users` VALUES
(1,1,'vishnu-iitp','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2','member','2025-06-10 19:40:13');

UNLOCK TABLES;
