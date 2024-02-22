-- Active: 1708404693781@@127.0.0.1@3306@login_user
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
DROP TABLE IF EXISTS accounts;
CREATE TABLE `accounts` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS comments;
CREATE TABLE `comments` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `author` int(100) NOT NULL,
  `post_id` int(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_auth_id` (`author`),
  KEY `fk_posttt_id` (`post_id`),
  CONSTRAINT `fk_auth_id` FOREIGN KEY (`author`) REFERENCES `accounts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_posttt_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS likes;
CREATE TABLE `likes` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `author` int(100) NOT NULL,
  `post_id` int(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_post_id` (`post_id`),
  KEY `fk_account_id` (`author`),
  CONSTRAINT `fk_account_id` FOREIGN KEY (`author`) REFERENCES `accounts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS post;
CREATE TABLE `post` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `author` int(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_author_id` (`author`),
  CONSTRAINT `fk_author_id` FOREIGN KEY (`author`) REFERENCES `accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO accounts(id,username,password,email,status) VALUES('1','\'hemaa_ai\'','\'hemaa1234\'','\'mibrahimmanagement@gmail.com\'','\'good health\''),('2','\'abdo\'','\'abdo1234\'','\'muebrahim1511@gmail.com\'','\'good health\''),('5','\'alisc\'','\'alisc1234\'','\'mibrahimmanagement@gmail.com\'','\'NULL\''),('6','\'abdelwhab\'','\'abdelwhab1234\'','\'muebrahim1511@gmail.com\'','\'NULL\'');


INSERT INTO post(id,text,author) VALUES('1','X\'68656c6c6f20677579732c200d0a63616e20736f6d65206f6e6520686572652068656c70206d6520746f2066696e64206120646f63746f7220696e2036206f63746f62657220636974792c2067697a610d0a7468616e6b73e29da4efb88f\'','2'),('2','X\'d8a7d984d8b3d984d8a7d98520d8b9d984d98ad983d98520d988d8b1d8add985d8a920d8a7d984d984d98720d988d8a8d8b1d983d8a7d8aad9870d0ad984d98820d8add8af20d985d8add8aad8a7d8ac20d8a3d98a20d985d8b3d8a7d8b9d8afd8a920d8a5d8add986d8a720d985d988d8acd988d8afd98ad98620d985d8b9d8a7d983d985\'','2'),('3','X\'68692065766572796f6e650d0a69276d206865726520666f7220796f752069662075206e65656420616e792068656c70\'','1');