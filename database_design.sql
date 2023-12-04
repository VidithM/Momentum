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
CREATE TABLE IF NOT EXISTS `momentum`.`posts` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `user` varchar(255) NOT NULL,
    `content` text NOT NULL,
    `community` VARCHAR(255) NOT NULL,
    `timestamp` DATETIME NOT NULL,
    `file` MEDIUMBLOB,
    PRIMARY KEY (`id`)
);
-- Sample Data
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
        "17",
        '2023-09-29 22:41:58',
        NULL
    );
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