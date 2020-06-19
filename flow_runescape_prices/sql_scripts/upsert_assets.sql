merge Runescape.dbo.assets as target
using (select * from
	(Values SELECTED_VALUES)
	as s (AssetName, AssetDisplayName)
	) as Source
on Target.AssetName = Source.AssetName
when not matched then
insert (AssetName, AssetDisplayName) values (Source.AssetName, Source.AssetDisplayName)
when matched then
update set AssetName = Source.AssetName, AssetDisplayName = Source.AssetDisplayName;