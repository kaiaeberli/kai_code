

declare @min_date datetime = '1Jan16'
declare @max_date datetime = '3Jan17'

/*
set @min_date = ? -- '1Jan16'
set @max_date = ? -- '1Jan17'
*/

set nocount on
set ansi_warnings off -- to remove message when avg ignores the NULL


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


where
    const.snaptime >= @min_date
    and const.snaptime <= @max_date
    
order by const.datestamp


