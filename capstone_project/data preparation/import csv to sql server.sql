

--q1-2011 is the last file that has two description columns

--declare @varDay as int = 1
declare @varMonth as int = 1
declare @varYear as int = 2000
declare @file as nvarchar(max)
declare @sqlstring as nvarchar(max)



while @varYear <> 2018

begin


	set @file = 'D:\Python Projects\kai_code\capstone_project\data\DAT_ASCII_EURUSD_T_' + convert(nvarchar,@varYear) + format(@varMonth, '0#')+'.csv'

	if @file not in ('sds')
	begin

		set @sqlstring = 

		'
		BULK INSERT dbo.fx_spot_data FROM '+CHAR(39)+@file+char(39)+'
			 WITH
			 (
				 FIELDTERMINATOR = '','',
				 ROWTERMINATOR = ''0x0A'',
				 MAXERRORS = 100,
				 DATAFILETYPE = ''char'',
				 KEEPIDENTITY
				 --FIRSTROW = 1
			 ) 
		 '
		 print(@sqlstring)
		 exec(@sqlstring)
		 
		 
	 end
	 
	 
	 --set @varDay= @varDay + 1
	 set @varMonth = @varMonth + 1
		 if @varMonth = 13
		 begin 
			set @varMonth = 1

			set @varYear = @varYear + 1
		 end


 
 end




--BULK INSERT dbo.fx_tick_data
--FROM 'D:\Python Projects\kai_code\capstone_project\data\DAT_ASCII_EURUSD_T_200005.csv'
----WITH (FORMAT = 'CSV'); 
--WITH  
--( 
--	FIELDTERMINATOR = ',',
--				 ROWTERMINATOR = '0x0A',
--				 MAXERRORS = 100,
--				 DATAFILETYPE = 'char',
--				 KEEPIDENTITY
--				 --FIRSTROW = 1
--);  