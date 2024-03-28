SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `student` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `student`;


DROP TABLE IF EXISTS `student`;
CREATE TABLE IF NOT EXISTS `student`(
    studentID int NOT NULL,
    studentUsername varchar(100) NOT NULL,
    studentName varchar(100) NOT NULL,
    studentEmail varchar(100) NOT NULL,
    phoneNum int NOT NULL,
    studentPassword varchar(100) NOT NULL,
    PRIMARY KEY (studentID)
)


