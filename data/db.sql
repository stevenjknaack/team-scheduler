CREATE DATABASE `10stars`;
USE `10stars`;
/*ADD Link to docs, change user primary key*/

CREATE TABLE `user` (
  `email` VARCHAR(255) PRIMARY KEY,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  CHECK (`email` LIKE '_%@_%._%')
);

CREATE UNIQUE INDEX `user_email_index`
ON `user` (`email`);

CREATE TABLE `availability_block` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `start_day` ENUM ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday') NOT NULL,
  `end_day` ENUM ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday') NOT NULL,
  `start_time` TIME NOT NULL,
  `end_time` TIME NOT NULL,
  `user_email` VARCHAR(255) NOT NULL, 
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE `availability_block` AUTO_INCREMENT = 10000;

CREATE INDEX `availability_block_user_email_index`
ON `availability_block` (`user_email`); 

CREATE TABLE `group` ( 
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50),
  `description` TEXT
);

ALTER TABLE `group` AUTO_INCREMENT = 10000;

CREATE INDEX `group_id_index`
ON `group` (`id`); 

CREATE TABLE `in_group` (
  `user_email` VARCHAR(255) NOT NULL,
  `group_id` INTEGER NOT NULL,
  `role` ENUM('invitee', 'participant', 'admin', 'owner') NOT NULL DEFAULT 'invitee',
  PRIMARY KEY (`user_email`, `group_id`),
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `team` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50),
  `description` TEXT,
  `group_id` INTEGER NOT NULL,
  UNIQUE (`id`, `group_id`),
  FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE `team` AUTO_INCREMENT = 10000;

CREATE INDEX `team_id_index`
ON `team` (`id`); 

CREATE INDEX `team_group_id_index`
ON `team` (`group_id`); 

CREATE TABLE `in_team` (
  `user_email` VARCHAR(255) NOT NULL,
  `team_id` INTEGER NOT NULL,
  PRIMARY KEY (`user_email`, `team_id`),
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `event` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `description` TEXT,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `reg_start_day` ENUM ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'),
  `reg_end_day` ENUM ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'),
  `start_time` TIME NOT NULL,
  `end_time` TIME NOT NULL,
  `edit_permission` ENUM ('member', 'group_admin') NOT NULL DEFAULT 'group_admin',
  `group_id` INTEGER,
  `team_id` INTEGER,
  CHECK (DATE(`start_date`) <= DATE(`end_date`)),
  CHECK ((`reg_start_day` IS NULL AND `reg_end_day` IS NULL)
  XOR (`reg_start_day` IS NOT NULL AND `reg_end_day` IS NOT NULL)),
  CHECK ((`group_id` IS NULL AND `team_id` IS NOT NULL)
  XOR (`group_id` IS NOT NULL AND `team_id` IS NULL)), 
  FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE `event` AUTO_INCREMENT = 10000;

CREATE UNIQUE INDEX `event_id_index`
ON `event` (`id`); 

CREATE TABLE `participates_in` (
  `user_email` VARCHAR(255) NOT NULL,
  `event_id` INTEGER NOT NULL,
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX `participates_in_user_email_index`
ON `participates_in` (`user_email`); 

CREATE INDEX `participates_in_event_id_index`
ON `participates_in` (`event_id`); 

/*CHECK ((`team_id` IS NULL AND `edit_permission` IS NULL) 
  XOR (`team_id` IS NOT NULL AND `edit_permission` IS NOT NULL)),*/