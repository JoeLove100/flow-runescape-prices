merge Runescape.dbo.assets as target
using (select * from
	(Values SELECTED_VALUES)
	as s (AssetName, AssetIndex)
	) as Source
on Target.AssetName = Source.AssetName
and Target.AssetIndex = Source.AssetIndex
when not matched then
insert (AssetName, AssetIndex, AssetDisplayName) values (Source.AssetName, Source.AssetIndex, Source.AssetDisplayName)
when matched then
update set AssetIndex = Source.AssetIndex, AssetName = Source.AssetName, AssetDisplayName = Source.AssetDisplayName;