CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

DROP TABLE IF EXISTS `stock_info`;
DROP TABLE IF EXISTS `stock_quotes`;

CREATE TABLE `stock_info` (
    `ticker` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `orgid` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `exgh` varchar(3) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `currency` varchar(3) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    KEY `ticker` (`ticker`,`orgid`),
    SHARD KEY `tick` (`ticker`)
);

CREATE TABLE `stock_quotes` (
    `ticker` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `dt` DATE NOT NULL,
    `open` DECIMAL(8,2) NOT NULL,
    `close` DECIMAL(8,2) NOT NULL,
    `high` DECIMAL(8,2) NOT NULL,
    `low` DECIMAL(8,2) NOT NULL,
    `inc` DECIMAL(8,2) NOT NULL,
    `vol` INT UNSIGNED NOT NULL,
    KEY `ticker` (`ticker`,`dt`),
    SHARD KEY `tick` (`ticker`)
);

