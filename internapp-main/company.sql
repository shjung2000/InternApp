SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `company` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `company`;


DROP TABLE IF EXISTS `company`;
CREATE TABLE IF NOT EXISTS `company`(
    companyID int NOT NULL,
    companyEmail varchar(100) NOT NULL,
    companyName varchar(100) NOT NULL,
    companyDesc varchar(100) NOT NULL,
    companySize int NOT NULL,
    companyPassword varchar(100) NOT NULL,
    PRIMARY KEY (companyID)
)