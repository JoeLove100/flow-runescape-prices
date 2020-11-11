merge Runescape.dbo.index_historic_prices as target
using( select * from
    (Values SELECTED_VALUES)
    as S (AsOfDate, IndexId, DataType, DataValue)
    ) as Source
on target.AsOfDate = Source.AsOfDate
and target.IndexId = Source.IndexId
and Target.DataType = Source.DataType
when not matched then
insert (AsOfDate, IndexId, DataType, DataValue) values (Source.AsOfDate, Source.IndexId, Source.DataType, Source.DataValue)
when matched then
update set DataValue = Source.DataValue;