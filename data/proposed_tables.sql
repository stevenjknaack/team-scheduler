use `10stars`;

CREATE TABLE `group` ( -- add 'group_name' optional column to event table for group level event
  `group_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `group_name` VARCHAR(50) NOT NULL DEFAULT 'Unnamed Group',
  `group_description` TEXT
);

CREATE TABLE `in_group` (
  `user_email` VARCHAR(255) NOT NULL,
  `group_id` INTEGER NOT NULL,
  `group_role` INTEGER NOT NULL DEFAULT 0,
  CHECK (0 <= `group_role` AND `group_role` <= 3),
  PRIMARY KEY (`user_email`, `group_id`),
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `team` ( -- add 'team_name' optional column to event table for team level event 
  `team_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `team_name` VARCHAR(50),
  `group_id` INTEGER NOT NULL,
  `team_description` TEXT,
  FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `in_team` (
  `user_email` VARCHAR(255) NOT NULL,
  `team_id` INTEGER NOT NULL,
  PRIMARY KEY (`user_email`, `team_id`),
  FOREIGN KEY (`user_email`) REFERENCES `user` (`email`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
  ON UPDATE CASCADE ON DELETE CASCADE
);