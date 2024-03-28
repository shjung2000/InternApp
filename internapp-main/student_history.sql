SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `record_one` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `record_one`;


DROP TABLE IF EXISTS `record_one`;
CREATE TABLE IF NOT EXISTS `record_one`(
    jobName varchar(100) NOT NULL,
    companyName varchar(100) NOT NULL,
    message varchar(100) NOT NULL,
    time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (jobName)
)







