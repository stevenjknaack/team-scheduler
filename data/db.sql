CREATE DATABASE `10stars`;
USE `10stars`;

CREATE TABLE `user` (
  `user_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `email` VARCHAR(255) UNIQUE,
  `username` VARCHAR(255),
  `password` VARCHAR(255)
);

CREATE TABLE `saved_event` (
  `event_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `event_name` VARCHAR(255),
  `start_date` DATE,
  `end_date` DATE,
  `start_time` TIME,
  `end_time` TIME,
  `event_description` TEXT,
  `owner_id` INTEGER,
  FOREIGN KEY (`owner_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `user_view` (
  `user_id` INTEGER PRIMARY KEY,
  `saved_event_id` INTEGER,
  `user_role` VARCHAR(10),
  FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  FOREIGN KEY (`saved_event_id`) REFERENCES `saved_event` (`event_id`)
);

CREATE TABLE `invitee` (
  `invitee_id` INTEGER,
  `queue_number` INTEGER,
  FOREIGN KEY (`invitee_id`) REFERENCES `user` (`user_id`)
);