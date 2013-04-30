-- phpMyAdmin SQL Dump
-- version 2.11.11.3
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 30, 2013 at 03:14 PM
-- Server version: 5.0.67
-- PHP Version: 5.1.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `bus`
--

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--
-- Creation: Apr 30, 2013 at 02:54 PM
-- Last update: Apr 30, 2013 at 03:09 PM
--

DROP TABLE IF EXISTS `predictions`;
CREATE TABLE IF NOT EXISTS `predictions` (
  `stopid` varchar(10) collate utf8_bin NOT NULL,
  `vehicleid` varchar(10) collate utf8_bin NOT NULL,
  `stopname` varchar(50) collate utf8_bin NOT NULL,
  `timestamp` bigint(20) NOT NULL,
  `busname` varchar(4) collate utf8_bin NOT NULL,
  PRIMARY KEY  (`stopid`,`vehicleid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

