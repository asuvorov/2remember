CREATE DATABASE IF NOT EXISTS `2remember`;
CREATE USER     IF NOT EXISTS root IDENTIFIED BY 'root';
CREATE USER     IF NOT EXISTS "ubuntu"@"localhost" IDENTIFIED BY "ubuntu";

GRANT ALL PRIVILEGES ON * . * TO "ubuntu"@"localhost";
