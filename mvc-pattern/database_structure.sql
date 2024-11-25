-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.40 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for tet
CREATE DATABASE IF NOT EXISTS `tet` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tet`;

-- Dumping structure for table tet.employees
CREATE TABLE IF NOT EXISTS `employees` (
  `EmployeeID` varchar(10) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(255) NOT NULL,
  PRIMARY KEY (`EmployeeID`),
  UNIQUE KEY `Email` (`Email`),
  KEY `idx_employee_email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table tet.employee_assignments
CREATE TABLE IF NOT EXISTS `employee_assignments` (
  `EmployeeAssignmentID` int NOT NULL AUTO_INCREMENT,
  `EmployeeID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ProjectID` int NOT NULL,
  PRIMARY KEY (`EmployeeAssignmentID`),
  KEY `EmployeeID` (`EmployeeID`),
  KEY `ProjectID` (`ProjectID`),
  CONSTRAINT `employee_assignments_ibfk_1` FOREIGN KEY (`EmployeeID`) REFERENCES `employees` (`EmployeeID`) ON DELETE CASCADE,
  CONSTRAINT `employee_assignments_ibfk_2` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table tet.projects
CREATE TABLE IF NOT EXISTS `projects` (
  `ProjectID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  PRIMARY KEY (`ProjectID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table tet.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `TaskID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `TaskStatus` varchar(50) NOT NULL,
  `CategoryID` int DEFAULT NULL,
  `RequirementNo` varchar(50) DEFAULT NULL,
  `IsShared` tinyint(1) NOT NULL DEFAULT '0',
  `Comment` text,
  `EstimationTime` int DEFAULT '0' COMMENT 'Auto cal',
  `TotalEffort` int DEFAULT '0' COMMENT 'Auto cal',
  `RemainingTime` int DEFAULT '0' COMMENT 'Auto cal',
  PRIMARY KEY (`TaskID`),
  KEY `idx_task_category` (`CategoryID`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `task_categories` (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table tet.task_assignments
CREATE TABLE IF NOT EXISTS `task_assignments` (
  `TaskAssignmentID` int NOT NULL AUTO_INCREMENT,
  `TaskID` int NOT NULL,
  `TaskAssignmentStatus` varchar(50) NOT NULL,
  `AssignedTime` timestamp NULL DEFAULT (now()),
  `EmployeeID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ProjectID` int NOT NULL,
  `ReviewFinding` int DEFAULT NULL,
  PRIMARY KEY (`TaskAssignmentID`),
  KEY `idx_task_assignment_task` (`TaskID`),
  KEY `idx_task_assignment_employee` (`EmployeeID`),
  CONSTRAINT `task_assignments_ibfk_1` FOREIGN KEY (`TaskID`) REFERENCES `tasks` (`TaskID`),
  CONSTRAINT `task_assignments_ibfk_2` FOREIGN KEY (`EmployeeID`) REFERENCES `employees` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table tet.task_categories
CREATE TABLE IF NOT EXISTS `task_categories` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `ProjectID` int NOT NULL,
  PRIMARY KEY (`CategoryID`),
  KEY `task_categories_ibfk_1` (`ProjectID`),
  CONSTRAINT `task_categories_ibfk_1` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table tet.time_entries
CREATE TABLE IF NOT EXISTS `time_entries` (
  `TimeEntryID` int NOT NULL AUTO_INCREMENT,
  `TaskAssignmentID` int NOT NULL,
  `Date` date NOT NULL,
  `Duration` decimal(5,2) NOT NULL,
  PRIMARY KEY (`TimeEntryID`),
  KEY `idx_time_entry_task_assignment` (`TaskAssignmentID`),
  CONSTRAINT `time_entries_ibfk_1` FOREIGN KEY (`TaskAssignmentID`) REFERENCES `task_assignments` (`TaskAssignmentID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
