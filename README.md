# Momentum Prototype

## Description with UI sketch of main use cases

### Description

### UI sketch file

## Database design

### Description of data entities and relationships

Data Entities: Comments, Communities, Posts, and Users.

At a high level, the relationships are as follows:

A user has:

1. rid: A record ID
2. name: the user's name
3. username
4. password
5. email
6. communities: The communities a user subscribes to
7. posts: The posts a user has made
8. comments: The comments a user has made.

A post has:

1. rid: A record id
2. user: The user who created the post
3. content: the text of the post
4. timestamp
5. community: the community a post is in
6. comments: any comments on the post
7. file: any attachments

A comment has:

1. rid: A record id
2. user: The user who created the pose
3. content: the text of the post
4. timestamp
5. parent: If this exists, the comment this comment replied to.
6. post: If this exists, the post the comment was made on.
7. comments: Any replies to this comment.

A community has:

1. rid: A unique identifier
2. description: Description of the community
3. users: the users in this community
4. posts: the posts made in this community.

However, as this is a graphql interface, some of these relationships can be done via graphql resolvers.
As a result, although at a high level a user has posts, the user table does not contain information about posts.
Rather, the GQL interface searches the posts table for all posts by a specific user when the front end wants the
posts by a user.  Additionally, although the posts and comments have unique keys, this is for database safety reasons -
they cannot exist without a user per the schema.

This is shown in more detail in the ERD.  Specifics of the tables are shown in the CREATE statements in the database design sql file,
rather than repeated here.

### Entity-relationship diagram file

![ERD](erd.jpg)

### SQL code to design database and sample data file

database_design.sql

```sql
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
```

## Architectural design

The momentum project is designed as a three tier archetecture.  The client is a Javascript server, which contains the GUI for user interactions.

The server itself is a graphql server, which manages interactions with the database and performs some of the relationship logic through resolvers.
This allows for a simpler table, as relationships don't need to be managed directly in the database.

The dabase is the third part of the architecture, and is a basic single schema four table Myswq database, run in a mariadb container.
As is common with industry databases, the database itself is not accessed outside of its specific API, in this case the gql server.

## Prototype

### Running the Momentum application

Instructions for the front and backends are in the README files in the respective folders.

GQL server: Momentum_gql
Application: Momentum_frontend

Database is run via docker-compose in momentup_gql.  Data and tables are not persistent, and will need to be added via the sql commands.

### Video recordings of user acceptance tests
