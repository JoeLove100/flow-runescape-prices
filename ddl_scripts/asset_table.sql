IF (NOT EXISTS (SELECT *
                 FROM INFORMATION_SCHEMA.TABLES
                 WHERE TABLE_SCHEMA = 'dbo'
                 AND  TABLE_NAME = 'assets'))
BEGIN
CREATE TABLE assets(
    AssetId int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    AssetName varchar(255) NOT NULL,
    AssetDisplayName varchar(255) NOT NULL
)
END