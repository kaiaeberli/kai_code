
--update const set row_num = row_number() over (order by snaptime asc)
--from kai_dw.dbo.fx_spot_data_features const
WITH upd AS
(
    SELECT
        row_num
        ,ROW_NUMBER() over (order by snaptime asc) seq
    FROM kai_dw.dbo.fx_spot_data_features const
)
UPDATE upd
SET row_num = Seq
