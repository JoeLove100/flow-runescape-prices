with tmp as (select * from (Values SELECTED_VALUES) as s (IndexId, AssetName))

MERGE Runescape.dbo.index_assets AS target
USING (
    select tmp.IndexId, assets.AssetId from tmp
    left join
    (select AssetName, AssetId from Runescape.dbo.assets) as assets
    on assets.AssetName = tmp.AssetName
    ) as Source
on Target.IndexId = Source.IndexId
and Target.AssetId = Source.AssetId
when not matched then
    insert (IndexId, AssetId) values (Source.IndexId, Source.AssetId);
