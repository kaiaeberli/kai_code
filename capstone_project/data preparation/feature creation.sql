

select
	
	const.snaptime
	, const.bid_price
	, const.ask_price
	, datepart(month, const.snaptime) 'month'
	, datepart(year, const.snaptime) 'year'
	, datepart(WEEK, const.snaptime) 'week'
	, datepart(HOUR, const.snaptime) 'hour'
	, datepart(day, const.snaptime) 'day'
	, datepart(WEEKDAY, const.snaptime) 'weekday'
	, datepart(MINUTE, const.snaptime) 'minute'
	, datepart(QUARTER, const.snaptime) 'quarter'
	, ROW_NUMBER() over (order by snaptime asc) 'row_num'


	--, count(*)
into kai_dw.dbo.fx_spot_data_features

--drop table kai_dw.dbo.fx_spot_data_features
from kai_dw.dbo.fx_spot_data_typed const

--group by const.snaptime
--order by 2 desc



/*
select top 100
	
	const.year, const.month, const.day, const.hour, round(const.minute/15,0) * 15
	, max(const.bid_price) 'high'
	, min(const.bid_price) 'low'
	, min(const.snaptime) 'open_datetime'
	, max(const.snaptime) 'close_datetime'
	, count(*)
	--, max(constMin.bid_price)

from kai_dw.dbo.fx_spot_data_features const
--left join kai_dw.dbo.fx_spot_data_features constMin
--	on constMin.snaptime = max(const.snaptime)

group by const.year, const.month, const.day, const.hour, round(const.minute/15,0)
order by const.year, const.month, const.day, const.hour, round(const.minute/15,0)
*/

--select round(datepart(minute, '2000-05-30 20:57:47.000')  /15, 0) * 15

USE [kai_dw]

GO

CREATE NONCLUSTERED INDEX [NonClusteredIndex-20171112-181301] ON [dbo].[fx_spot_data_features]
(
	[snaptime] ASC,
	[row_num] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

GO


select count(*) from kai_dw.dbo.fx_spot_data_features
select count(*) from kai_dw.dbo.fx_spot_data_typed
select count(*) from kai_dw.dbo.fx_spot_data


