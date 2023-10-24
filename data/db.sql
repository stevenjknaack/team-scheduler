CREATE DATABASE `10stars`;
USE `10stars`;

CREATE TABLE `user` (
  `email` VARCHAR(255) PRIMARY KEY,
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
  FOREIGN KEY (`owner_id`) REFERENCES `user` (`email`)
);

CREATE TABLE `user_view` (
  `user_id` INTEGER PRIMARY KEY,
  `saved_event_id` INTEGER,
  `user_role` VARCHAR(10),
  FOREIGN KEY (`user_id`) REFERENCES `user` (`email`),
  FOREIGN KEY (`saved_event_id`) REFERENCES `saved_event` (`event_id`)
);

CREATE TABLE `invitee` (
  'event_id' INTEGER,
  `email` VARCHAR(255) NOT NULL,
  FOREIGN KEY (`email`) REFERENCES `user` (`email`)
  FOREIGN KEY ('event_id') REFERENCES 'saved_event' ('event_id')
);