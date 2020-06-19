IF (NOT EXISTS (SELECT *
                 FROM INFORMATION_SCHEMA.TABLES
                 WHERE TABLE_SCHEMA = 'dbo'
                 AND  TABLE_NAME = 'index_assets'))
BEGIN
CREATE TABLE index_assets(
    IndexId int NOT NULL,
    AssetId int NOT NULL,
    PRIMARY KEY (IndexId, AssetId)
)
END