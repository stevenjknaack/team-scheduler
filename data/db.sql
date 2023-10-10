CREATE TABLE `adminView` (
  `user_id` integer,
  `saved_event_id` integer
);

CREATE TABLE `saved_event` (
  `event_id` integer,
  `event_name` varchar(255),
  `event_description` text,
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
  `username` varchar(255),
  `role` varchar(255),
  `created_at` timestamp
);

ALTER TABLE `adminView` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `userView` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `saved_event` ADD FOREIGN KEY (`event_id`) REFERENCES `adminView` (`saved_event_id`);

ALTER TABLE `saved_event` ADD FOREIGN KEY (`event_id`) REFERENCES `userView` (`saved_event_id`);

ALTER TABLE `invitee` ADD FOREIGN KEY (`invitee_id`) REFERENCES `saved_event` (`invitee_id`);

ALTER TABLE `invitee` ADD FOREIGN KEY (`invitee_id`) REFERENCES `users` (`id`);