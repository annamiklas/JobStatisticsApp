CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
	`password` varchar(255) NOT NULL,
	`email` varchar(50) NOT NULL,
    PRIMARY KEY(`id`)
)