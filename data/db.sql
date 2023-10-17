CREATE TABLE `saved_event` (
  `event_id` integer,
  `event_name` varchar(255),
  `time_range` varchar(255),
  `event_description` text,
  `admin_id` integer,
  `invitee_id` integer
);

CREATE TABLE `userView` (
  `user_id` integer PRIMARY KEY,
  `saved_event_id` integer
);

CREATE TABLE `invitee` (
  `invitee_id` integer,
  `queue_number` integer
);

CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `email` varchar(255),
  `username` varchar(255),
  `password` varchar(255)
);

ALTER TABLE `userView` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `saved_event` ADD FOREIGN KEY (`event_id`) REFERENCES `userView` (`saved_event_id`);

ALTER TABLE `invitee` ADD FOREIGN KEY (`invitee_id`) REFERENCES `saved_event` (`invitee_id`);

ALTER TABLE `invitee` ADD FOREIGN KEY (`invitee_id`) REFERENCES `users` (`id`);

ALTER TABLE `saved_event` ADD FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`);
