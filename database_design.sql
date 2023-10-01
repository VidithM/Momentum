-- Create Statements
CREATE TABLE IF NOT EXISTS `momentum`.`comments` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `user` varchar(255) NOT NULL,
    `content` TEXT NOT NULL,
    `parent` int(10),
    `timestamp` DATETIME NOT NULL,
    `post` int(10),
    PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `momentum`.`communities` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `description` text,
    `users` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `momentum`.`posts` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `user` varchar(255) NOT NULL,
    `content` text NOT NULL,
    `community` int(10) NOT NULL,
    `timestamp` DATETIME NOT NULL,
    `file` MEDIUMBLOB,
    PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `momentum`.`users` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `communities` text,
    `password` varchar(255) NOT NULL,
    `username` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);
-- Sample Data
INSERT INTO `users` (
        `id`,
        `communities`,
        `password`,
        `username`,
        `name`,
        `email`
    )
VALUES (
        17,
        '17',
        'password',
        'nmcclaran',
        'Nathan McClaran',
        'nmcclaran@tamu.edu'
    );
INSERT INTO `posts` (
        `id`,
        `user`,
        `content`,
        `community`,
        `timestamp`,
        `file`
    )
VALUES (
        1,
        '17',
        'nmcclaran_3',
        17,
        '2023-09-29 22:41:58',
        NULL
    );
INSERT INTO `communities` (`id`, `description`, `users`)
VALUES (17, 'nmcclaran_2', '17');
INSERT INTO `comments` (
        `id`,
        `user`,
        `content`,
        `parent`,
        `timestamp`,
        `post`
    )
VALUES (
        1,
        '17',
        'nmcclaran_2',
        NULL,
        '2023-09-29 22:41:58',
        1
    ),
    (
        2,
        '17',
        'nmcclaran_2',
        NULL,
        '2023-09-29 22:41:58',
        1
    ),
    (
        3,
        '17',
        'nmcclaran_2',
        NULL,
        '2023-09-29 22:41:58',
        1
    );