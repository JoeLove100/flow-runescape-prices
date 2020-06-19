IF (NOT EXISTS (SELECT *
                 FROM INFORMATION_SCHEMA.TABLES
                 WHERE TABLE_SCHEMA = 'dbo'
                 AND  TABLE_NAME = 'indices'))
BEGIN
CREATE TABLE indices(
    IndexId int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    IndexName varchar(255) NOT NULL,
    IndexDisplayName varchar(255) NOT NULL,
    IsIncluded bit NOT NULL
)
END