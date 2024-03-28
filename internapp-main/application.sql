SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `application` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `application`;

DROP TABLE IF EXISTS `application`;
CREATE TABLE IF NOT EXISTS `application`(
    applicationID int NOT NULL,
    companyID int NOT NULL,
    studentID int NOT NULL,
    jobID int NOT NULL,
    coverletter varchar(1000) NOT NULL,
    applicationStatus varchar(20) NOT NULL,
    PRIMARY KEY (applicationID),
    KEY FK_companyID (companyID),
    KEY FK_studentID (studentID),
    KEY FK_jobID (jobID)
)