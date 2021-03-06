/****** Script for SelectTopNRows command from SSMS  ******/
SELECT --TOP (1000) 
	
	
	
	 convert(datetime, 
		left([snaptime], 4) + '-'
		+ substring([snaptime], 5,2) +'-' --month
		+ substring([snaptime], 7,2) +' ' -- day
		+ substring([snaptime], 10, 2) +':'
		+ substring([snaptime], 12, 2) +':'
		+ substring([snaptime], 14, 2) +':'
		+ substring([snaptime], 16, 3) 

		, 121) [snaptime]
		--	yyyy-mm-dd hh:mi:ss.mmm
	--  ,[snaptime]
      ,[bid_price]
      ,[ask_price]
      ,[volume]


into dbo.fx_spot_data_typed
FROM [kai_dw].[dbo].[fx_spot_data]