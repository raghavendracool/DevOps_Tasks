-- Task 11: Create the application database and restricted user.
-- Replace the example password before execution.

CREATE DATABASE IF NOT EXISTS appdb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'appuser'@'%'
  IDENTIFIED BY 'REPLACE_WITH_STRONG_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE
ON appdb.*
TO 'appuser'@'%';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'appuser'@'%';
