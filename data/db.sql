CREATE DATABASE `10stars`;
USE `10stars`;

CREATE TABLE `user` (
  `email` VARCHAR(255) PRIMARY KEY,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL
);

CREATE UNIQUE INDEX `user_email_index`
ON `user` (`email`); 

-- insert proposed_tables here

CREATE TABLE `event` (
  `event_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `event_name` VARCHAR(255) NOT NULL DEFAULT 'Unnamed Event',
  `start_date` DATE,
  `end_date` DATE,
  `start_time` TIME,
  `end_time` TIME,
  `event_description` TEXT,
  /*`group_id` INTEGER,
  `team_id` INTEGER,
  FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
  ON UPDATE CASCADE ON DELETE CASCADE*/
);

CREATE UNIQUE INDEX `event_id_index`
ON `event` (`event_id`); 

CREATE TABLE `participates_in` (
  `user_email` VARCHAR(255) NOT NULL,
  `event_id` INTEGER NOT NULL,
  `user_role` INTEGER NOT NULL DEFAULT 0,
  CHECK (0 <= `user_role` AND `user_role` <= 3),
  PRIMARY KEY (`user_email`, `event_id`),
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `participates_in_user_email_index`
ON `participates_in` (`user_email`); 

CREATE INDEX `participates_in_event_id_index`
ON `participates_in` (`event_id`); 