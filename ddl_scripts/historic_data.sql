IF (NOT EXISTS (SELECT *
                 FROM INFORMATION_SCHEMA.TABLES
                 WHERE TABLE_SCHEMA = 'dbo'
                 AND  TABLE_NAME = 'historic_data'))
BEGIN
CREATE TABLE historic_data(
    DataId int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    AsOfDate date NOT NULL,
    AssetId int NOT NULL,
    DataType varchar(255) NOT NULL,
    DataValue float NOT NULL
)
END