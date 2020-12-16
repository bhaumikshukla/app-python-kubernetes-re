Create database sampledb;
CREATE TABLE sampledb.myguests (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
email VARCHAR(50));

insert into sampledb.myguests (firstname, lastname, email) values ('Unnati','Shukla','unnati@def.com');
insert into sampledb.myguests (firstname, lastname, email) values ('Bhaumik','Shukla','bhaumik@def.com');
