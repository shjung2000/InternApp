SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `job` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `job`;

DROP TABLE IF EXISTS `job`;
CREATE TABLE IF NOT EXISTS `job`(
    jobID int NOT NULL,
    companyID int NOT NULL,
    jobName varchar(100) NOT NULL,
    postDate date NOT NULL,
    jobDesc varchar(1000) NOT NULL,
	deadline datetime NOT NULL,
    PRIMARY KEY (jobID),
    KEY FK_companyID (companyID)
)





