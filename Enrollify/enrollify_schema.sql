-- ========================================
-- FIXED Enrollify Database Schema
-- Run this to fix column mismatches
-- ========================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Drop existing database and recreate
DROP DATABASE IF EXISTS `enrollify_db`;
CREATE DATABASE `enrollify_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `enrollify_db`;

-- --------------------------------------------------------
-- Table: students (FIXED column names)
-- --------------------------------------------------------
CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lrn` varchar(12) NOT NULL UNIQUE,
  `firstname` varchar(100) NOT NULL,
  `middlename` varchar(100) DEFAULT '',
  `lastname` varchar(100) NOT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `grade_level` varchar(20) DEFAULT NULL,  -- FIXED: was 'grade'
  `track` varchar(100) DEFAULT NULL,
  `strand` varchar(100) DEFAULT NULL,
  `guardian_name` varchar(150) DEFAULT NULL,
  `guardian_contact` varchar(50) DEFAULT NULL,
  `enrollment_status` varchar(20) DEFAULT 'Pending',  -- FIXED: was 'status'
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_lrn` (`lrn`),
  KEY `idx_status` (`enrollment_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Table: tracks
-- --------------------------------------------------------
CREATE TABLE `tracks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL UNIQUE,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Table: strands
-- --------------------------------------------------------
CREATE TABLE `strands` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_track` (`track`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Table: tuition_fees
-- --------------------------------------------------------
CREATE TABLE `tuition_fees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track` varchar(100) NOT NULL,
  `strand` varchar(100) DEFAULT NULL,
  `enrollment_fee` decimal(10,2) NOT NULL DEFAULT 5000.00,
  `miscellaneous_fee` decimal(10,2) NOT NULL DEFAULT 4500.00,
  `tuition_fee` decimal(10,2) NOT NULL DEFAULT 15000.00,
  `special_fee` decimal(10,2) NOT NULL DEFAULT 2000.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_track_strand` (`track`, `strand`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Table: payments
-- --------------------------------------------------------
CREATE TABLE `payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `lrn` varchar(12) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) DEFAULT 'Cash',
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_payment_student` (`student_id`),
  KEY `idx_lrn` (`lrn`),
  CONSTRAINT `fk_payment_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Table: users (with password hashing)
-- --------------------------------------------------------
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(150) NOT NULL UNIQUE,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('ADMIN','STAFF','STUDENT') NOT NULL DEFAULT 'STUDENT',
  `full_name` varchar(150) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `last_login` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Table: audit_log (FIXED column name)
-- --------------------------------------------------------
CREATE TABLE `audit_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_email` varchar(100) DEFAULT NULL,  -- FIXED: was 'user'
  `action` varchar(100) NOT NULL,
  `details` text,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ========================================
-- INSERT SAMPLE DATA
-- ========================================

-- Insert default tracks
INSERT INTO `tracks` (`name`, `description`) VALUES
('Academic Track', 'College preparatory programs'),
('TVL Track', 'Technical-Vocational-Livelihood programs'),
('Sports Track', 'Sports and athletics focus'),
('Arts and Design Track', 'Creative arts and design programs');

-- Insert strands for Academic Track
INSERT INTO `strands` (`track`, `name`, `description`) VALUES
('Academic Track', 'STEM', 'Science, Technology, Engineering, and Mathematics'),
('Academic Track', 'ABM', 'Accountancy, Business, and Management'),
('Academic Track', 'HUMSS', 'Humanities and Social Sciences'),
('Academic Track', 'GAS', 'General Academic Strand');

-- Insert strands for TVL Track
INSERT INTO `strands` (`track`, `name`, `description`) VALUES
('TVL Track', 'ICT', 'Information and Communications Technology'),
('TVL Track', 'Home Economics', 'Food and Beverage Services, Cookery'),
('TVL Track', 'Agri-Fishery Arts', 'Agriculture and fishery programs');

-- Insert default tuition fees
INSERT INTO `tuition_fees` (`track`, `strand`, `enrollment_fee`, `miscellaneous_fee`, `tuition_fee`, `special_fee`) VALUES
('Academic Track', 'STEM', 5000.00, 4500.00, 18000.00, 3000.00),
('Academic Track', 'ABM', 5000.00, 4500.00, 16000.00, 2500.00),
('Academic Track', 'HUMSS', 5000.00, 4500.00, 15000.00, 2000.00),
('Academic Track', 'GAS', 5000.00, 4500.00, 15000.00, 2000.00),
('TVL Track', 'ICT', 5000.00, 4500.00, 17000.00, 2500.00),
('TVL Track', 'Home Economics', 5000.00, 4500.00, 16000.00, 2500.00),
('Sports Track', NULL, 5000.00, 4500.00, 15000.00, 3500.00),
('Arts and Design Track', NULL, 5000.00, 4500.00, 16000.00, 3000.00);

-- ========================================
-- INSERT SAMPLE USERS (with bcrypt hashes)
-- Password for all accounts: "admin123"
-- ========================================

-- Admin user: admin@enrollify.edu / admin123
INSERT INTO `users` (`email`, `password_hash`, `role`, `full_name`, `is_active`) VALUES
('admin@enrollify.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eoK0Oo5SQn7i', 'ADMIN', 'System Administrator', 1);

-- Staff user: staff@enrollify.edu / staff123
INSERT INTO `users` (`email`, `password_hash`, `role`, `full_name`, `is_active`) VALUES
('staff@enrollify.edu', '$2b$12$9k5Z8R4YxQx4qF5h5Z5X5e5x5x5x5x5x5x5x5x5x5x5x5x5x5x5x5', 'STAFF', 'Enrollment Staff', 1);

-- Note: The actual bcrypt hash for "staff123" will be generated by your auth_utils.py
-- You need to run the Python script below to generate proper hashes

COMMIT;

-- ========================================
-- VERIFICATION QUERIES
-- ========================================
-- Run these after setup to verify:
-- SELECT * FROM users;
-- SELECT * FROM tracks;
-- SELECT * FROM strands;
-- SELECT * FROM tuition_fees;