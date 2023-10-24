CREATE DATABASE `10stars`;
USE `10stars`;

CREATE TABLE `user` (
  `email` VARCHAR(255) PRIMARY KEY,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL
);

CREATE TABLE `event` (
  `event_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `event_name` VARCHAR(255) NOT NULL DEFAULT 'Unnamed Event',
  `start_date` DATE,
  `end_date` DATE,
  `start_time` TIME,
  `end_time` TIME,
  `event_description` TEXT NOT NULL DEFAULT 'No description added.',
  `creator_email` VARCHAR(255) NOT NULL,
  FOREIGN KEY (`creator_email`) REFERENCES `user` (`email`)
);

CREATE TABLE `participates_in` (
  `user_email` VARCHAR(255) NOT NULL,
  `event_id` INTEGER NOT NULL,
  `user_role` INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_email`, `event_id`),
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`),
  FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`)
);