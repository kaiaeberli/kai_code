

declare @min_date datetime = '1Jan16'
declare @max_date datetime = '1Jan17'

/*
set @min_date = ? -- '1Jan16'
set @max_date = ? -- '1Jan17'
*/

set nocount on
drop table kai_dw.dbo.fx_spot_data_15_min 

--insert into kai_dw.dbo.fx_spot_data_15_min 
select
    --distinct
    const.year, const.month, const.day, const.hour, const.weekday, round(const.minute/15,0) * 15 '15_min'
	, DATETIMEFROMPARTS(const.year, const.month, const.day, const.hour, round(const.minute/15,0) * 15, 0, 0) 'datestamp'
	
    --, const.snaptime 'date'
    --, const.bid_price
    --, const.ask_price
    --, const.ask_price - const.bid_price 'bo_spread'
	, max(const.bid_price) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0))'high_bid'
	, min(const.bid_price) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0)) 'low_bid'
    , avg(const.ask_price - const.bid_price) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0)) 'avg_bo_spread'
	--, min(const.snaptime) 'open_datetime'
	--, max(const.snaptime) 'close_datetime'
	, count(*) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0)) 'nb_ticks'
    , first_value(const.bid_price) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0) order by const.snaptime asc rows between unbounded preceding and unbounded following) 'open_bid'
	, last_value(const.bid_price) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0) order by const.snaptime asc rows between unbounded preceding and unbounded following) 'close_bid'

    -- this is current bid price 
	, const.bid_price
	, constPrev.bid_price 'bid_price_prev'
	, const.ask_price
	, const.snaptime
	, constPrev.snaptime 'snaptime_prev'
	
	, row_number() over  (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0) order by const.snaptime desc) row_num_window
	--, max(const.bid_price) over (partition by const.year, const.month, const.day, const.hour, round(const.minute/15,0) order by const.snaptime asc) 'close'

into kai_dw.dbo.fx_spot_data_15_min
from kai_dw.dbo.fx_spot_data_features const
left join kai_dw.dbo.fx_spot_data_features constPrev
	on const.row_num = constPrev.row_num - 1

where
    const.snaptime >= @min_date
    and const.snaptime <= @max_date
    
--group by const.year, const.month, const.day, const.hour, round(const.minute/15,0)
order by const.year, const.month, const.day, const.hour, 6
--order by const.snaptime



--select * from #tmp1
select
distinct
    const.[year]
	, const.[month]
	, const.[day]
	, const.[hour]
	, const.[weekday]
	, const.[15_min]
	, const.datestamp
	
    
	, const.high_bid
	, const.low_bid
    , const.avg_bo_spread
	, const.nb_ticks
    , const.[open_bid]
	, const.[close_bid]

	-- last 5 ticks return average
    
	-- this is current bid price 
	--, const.bid_price
	--, const.snaptime
	
	--, const.row_num_window
	, avg(case when const.row_num_window <= 10 then const.bid_price / const.bid_price_prev-1 else NULL end) over (partition by const.datestamp) 'last_10_tick_avg_bid_return'
	, avg(case when const.row_num_window <= 10 then const.ask_price - const.bid_price else NULL end) over (partition by const.datestamp) 'last_10_tick_avg_bo_spread'


from kai_dw.dbo.fx_spot_data_15_min const
order by const.datestamp
