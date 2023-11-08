-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 12, 2023 at 05:05 PM
-- Server version: 8.0.33
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cp`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `countfun` ()   BEGIN
select COUNT(Year) As NoStudents from students where Year = 2;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `myprocedure` ()   begin
select * from students;
insert into students(PRN, Name, Year, Mail,Github, LinkedIn,Bio)
values
(12210123,"Kush Bhakkad", 2, "aditya.adaki22@vit.edu","https://github.com/adityaadaki","https://linkedin.com/in/adityaadaki",NULL),
(12210318, "Pranit Chilbule", 2, "pranit.chilbule22@vit.edu", "https://github.com/pranitchilbule","https://linkedin.com/in/pranitchilbule",NULL);
select * from students;
delete from students where Mail ='aditya.adaki22@vit.edu';
select * from students;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `answers`
--

CREATE TABLE `answers` (
  `Q_ID` int NOT NULL,
  `A_ID` int NOT NULL,
  `PRN` int NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Answer` text NOT NULL,
  `AvgRating` decimal(5,2) DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `answers`
--

INSERT INTO `answers` (`Q_ID`, `A_ID`, `PRN`, `Timestamp`, `Answer`, `AvgRating`) VALUES
(1, 1, 12211318, '2023-08-15 05:15:00', 'Encapsulation in OOP refers to...', 4.50),
(1, 2, 12211315, '2023-08-15 05:45:00', 'Encapsulation ensures...', 4.00),
(2, 3, 12211320, '2023-08-15 06:15:00', 'Web development encompasses...', 4.50),
(3, 4, 12211325, '2023-08-15 07:00:00', 'Normalization in DBMS is the process of...', 4.00),
(3, 5, 12211330, '2023-08-15 07:30:00', 'Normalization helps in reducing...', 4.50),
(4, 6, 12211335, '2023-08-15 08:30:00', 'A stack can be implemented using arrays...', 5.00),
(4, 7, 12211340, '2023-08-15 09:00:00', 'Arrays provide a simple and efficient...', 0.00),
(5, 8, 12211345, '2023-08-15 09:30:00', 'Mobile app components include...', 0.00),
(5, 9, 12211350, '2023-08-15 10:00:00', 'User interface design, backend services...', 0.00),
(6, 10, 12211355, '2023-08-15 10:30:00', 'IoT and Blockchain have various applications...', 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `domains`
--

CREATE TABLE `domains` (
  `D_ID` int NOT NULL,
  `Domain` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `domains`
--

INSERT INTO `domains` (`D_ID`, `Domain`) VALUES
(1, 'Leadership'),
(2, 'Time management'),
(3, 'Public Speaking'),
(4, 'OOPs'),
(5, 'DBMS'),
(6, 'IoT and Blockchain'),
(7, 'DSA'),
(8, 'Web Development'),
(9, 'App Development'),
(10, 'AI/ML/DS'),
(11, 'Other');

-- --------------------------------------------------------

--
-- Table structure for table `expertise`
--

CREATE TABLE `expertise` (
  `PRN` int NOT NULL,
  `Expertise` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `expertise`
--

INSERT INTO `expertise` (`PRN`, `Expertise`) VALUES
(12211315, 1),
(12211318, 3),
(12211320, 8),
(12211325, 5),
(12211330, 2),
(12211335, 6),
(12211340, 10),
(12211345, 7),
(12211350, 9),
(12211355, 11);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `Q_ID` int NOT NULL,
  `D_ID` int DEFAULT NULL,
  `PRN` int NOT NULL,
  `Timestamp` timestamp NOT NULL,
  `Question` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`Q_ID`, `D_ID`, `PRN`, `Timestamp`, `Question`) VALUES
(1, 4, 12211315, '2023-08-15 04:00:00', 'How does encapsulation work in OOP?'),
(2, 8, 12211318, '2023-08-15 04:45:00', 'What are the key concepts of web development?'),
(3, 5, 12211320, '2023-08-15 05:30:00', 'Explain the normalization process in DBMS.'),
(4, 7, 12211325, '2023-08-15 06:30:00', 'How do you implement a stack using arrays?'),
(5, 9, 12211330, '2023-08-15 08:00:00', 'What are the main components of a mobile app?'),
(6, 6, 12211335, '2023-08-15 09:15:00', 'Discuss the applications of IoT and Blockchain.'),
(7, 10, 12211340, '2023-08-15 10:00:00', 'What\'s the difference between AI, ML, and Data Science?'),
(8, 3, 12211345, '2023-08-15 10:30:00', 'How can I improve my public speaking skills?'),
(9, 2, 12211350, '2023-08-15 11:15:00', 'Share tips for effective time management.'),
(11, 2, 12211355, '2023-10-10 17:14:09', 'What is Swing?');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `A_ID` int NOT NULL,
  `PRN` int NOT NULL,
  `Rating` int DEFAULT NULL,
  `Comment` text,
  `Timestamp` timestamp NOT NULL
) ;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`A_ID`, `PRN`, `Rating`, `Comment`, `Timestamp`) VALUES
(1, 12211315, 5, 'Great explanation!', '2023-08-16 03:30:00'),
(1, 12211318, 4, 'Helpful answer.', '2023-08-16 03:45:00'),
(2, 12211320, 4, 'Clear and concise.', '2023-08-16 04:30:00'),
(3, 12211325, 5, 'Detailed response, thank you!', '2023-08-16 05:00:00'),
(3, 12211330, 4, 'Could use more examples.', '2023-08-16 05:30:00'),
(4, 12211335, 5, 'Explained well, thank you!', '2023-08-16 06:00:00'),
(4, 12211340, 3, 'Could be more detailed.', '2023-08-16 06:30:00'),
(5, 12211345, 5, 'Great overview of app components.', '2023-08-16 07:00:00'),
(5, 12211350, 4, 'Could include more backend details.', '2023-08-16 07:30:00'),
(6, 12211355, 5, 'Informative, thanks!', '2023-08-16 08:00:00');

--
-- Triggers `reviews`
--
DELIMITER $$
CREATE TRIGGER `after_review_update` AFTER UPDATE ON `reviews` FOR EACH ROW begin
    DECLARE total_ratings INT;
    DECLARE total_rating_value DECIMAL(5, 2);

    
    SELECT COUNT(*), SUM(Rating)
    INTO total_ratings, total_rating_value
    FROM reviews
    WHERE A_ID = NEW.A_ID;

    
    IF total_ratings > 0 THEN
        UPDATE answers
        SET AvgRating = total_rating_value / total_ratings
        WHERE A_ID = NEW.A_ID;
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_answer_avg_rating` AFTER INSERT ON `reviews` FOR EACH ROW BEGIN
    
    DECLARE total_ratings INT;
    DECLARE total_rating_value DECIMAL(5, 2);

    
    SELECT COUNT(*), SUM(Rating)
    INTO total_ratings, total_rating_value
    FROM reviews
    WHERE A_ID = NEW.A_ID;

    
    IF total_ratings > 0 THEN
        UPDATE answers
        SET AvgRating = total_rating_value / total_ratings
        WHERE A_ID = NEW.A_ID;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `PRN` int NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Year` int DEFAULT NULL,
  `Mail` varchar(255) DEFAULT NULL,
  `GitHub` varchar(255) DEFAULT NULL,
  `LinkedIn` varchar(255) DEFAULT NULL,
  `Bio` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`PRN`, `Name`, `Year`, `Mail`, `GitHub`, `LinkedIn`, `Bio`) VALUES
(12210318, 'Pranit Chilbule', 2, 'pranit.chilbule22@vit.edu', 'https://github.com/pranitchilbule', 'https://linkedin.com/in/pranitchilbule', NULL),
(12210428, 'Aditya Adaki', 2, 'aditya.adaki22@vit.edu', 'https://github.com/adityaadaki', 'https://linkedin.com/in/adityaadaki', NULL),
(12211315, 'John Doe', 1, 'ab.cd221@vit.edu', 'https://github.com/johndoe', 'https://linkedin.com/in/johndoe', NULL),
(12211318, 'Jane Smith', 2, 'ef.gh22@vit.edu', 'https://github.com/janesmith', 'https://linkedin.com/in/janesmith', NULL),
(12211320, 'Michael Johnson', 4, 'kl.mn223@vit.edu', 'https://github.com/michaeljohnson', 'https://linkedin.com/in/michaeljohnson', NULL),
(12211325, 'Emily White', 3, 'op.qr224@vit.edu', 'https://github.com/emilywhite', 'https://linkedin.com/in/emilywhite', NULL),
(12211330, 'Robert Brown', 1, 'st.uv225@vit.edu', 'https://github.com/robertbrown', 'https://linkedin.com/in/robertbrown', NULL),
(12211335, 'Olivia Davis', 4, 'wx.yz226@vit.edu', 'https://github.com/oliviadavis', 'https://linkedin.com/in/oliviadavis', NULL),
(12211340, 'William Wilson', 3, 'ab.cd227@vit.edu', 'https://github.com/williamwilson', 'https://linkedin.com/in/williamwilson', NULL),
(12211345, 'Sophia Martinez', 2, 'ef.gh228@vit.edu', 'https://github.com/sophiamartinez', 'https://linkedin.com/in/sophiamartinez', NULL),
(12211350, 'Liam Taylor', 1, 'kl.mn229@vit.edu', 'https://github.com/liamtaylor', 'https://linkedin.com/in/liamtaylor', NULL),
(12211355, 'Ava Anderson', 3, 'op.qr230@vit.edu', 'https://github.com/avaanderson', 'https://linkedin.com/in/avaanderson', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `answers`
--
ALTER TABLE `answers`
  ADD PRIMARY KEY (`A_ID`),
  ADD KEY `PRN` (`PRN`),
  ADD KEY `answers_ibfk_2` (`Q_ID`);

--
-- Indexes for table `domains`
--
ALTER TABLE `domains`
  ADD PRIMARY KEY (`D_ID`);

--
-- Indexes for table `expertise`
--
ALTER TABLE `expertise`
  ADD KEY `PRN` (`PRN`),
  ADD KEY `Expertise` (`Expertise`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`Q_ID`),
  ADD KEY `PRN` (`PRN`),
  ADD KEY `Domain` (`D_ID`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD KEY `PRN` (`PRN`),
  ADD KEY `reviews_ibfk_1` (`A_ID`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`PRN`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `answers`
--
ALTER TABLE `answers`
  MODIFY `A_ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `Q_ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `answers`
--
ALTER TABLE `answers`
  ADD CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`PRN`) REFERENCES `students` (`PRN`),
  ADD CONSTRAINT `answers_ibfk_2` FOREIGN KEY (`Q_ID`) REFERENCES `questions` (`Q_ID`);

--
-- Constraints for table `expertise`
--
ALTER TABLE `expertise`
  ADD CONSTRAINT `expertise_ibfk_1` FOREIGN KEY (`PRN`) REFERENCES `students` (`PRN`),
  ADD CONSTRAINT `expertise_ibfk_2` FOREIGN KEY (`Expertise`) REFERENCES `domains` (`D_ID`);

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`PRN`) REFERENCES `students` (`PRN`),
  ADD CONSTRAINT `questions_ibfk_2` FOREIGN KEY (`D_ID`) REFERENCES `domains` (`D_ID`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`A_ID`) REFERENCES `answers` (`A_ID`),
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`PRN`) REFERENCES `students` (`PRN`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
