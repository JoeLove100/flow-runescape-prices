merge Runescape.dbo.historic_data as target
using (select * from
	(Values SELECTED_VALUES)
	as s (AsOfDate, AssetId, DataType, DataValue)
	) as Source
on Target.AsOfDate = Source.AsOfDate
and Target.AssetId = Source.AssetId
and Target.DataType = Source.DataType
when not matched then
insert (AsOfDate, AssetId, DataType, DataValue) values (Source.AsOfDate, Source.AssetId, Source.DataType, Source.DataValue)
when matched then
update set DataValue = Source.DataValue;