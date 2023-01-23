
query_calc_statistics = """
select date, count(count_to_redirect) as count_of_messages, sum(count_to_redirect) as count_of_operators from
(
select t2.date,
       (case when sum(redirect_bool) > 0 then 1 else 0 end ) as count_to_redirect from

(select t.date,
       dense_rank() over (order by minid) as new_id,
              (CASE
                  WHEN (jsonb_extract_path(t.dirty_data,'replies','0','body', 'items', '0', 'command', 'action', 'type') IS NULL
                            AND jsonb_extract_path(t.dirty_data,'replies','2','body', 'items', '0', 'command', 'action', 'type') IS NULL
                      AND jsonb_extract_path(t.dirty_data,'replies','1','body', 'items', '0', 'command', 'action', 'type') IS NULL
                             AND jsonb_extract_path(t.dirty_data,'replies','3','body', 'items', '0', 'command', 'action', 'type') IS NULL
                      AND jsonb_extract_path(t.dirty_data,'replies','4','body', 'items', '0', 'command', 'action', 'type') IS NULL)
                      THEN 0 ELSE 1 END) as redirect_bool
from (select t.*, min(id) over (partition by message_name, grp) as minid
      from (select t.*,
                   (row_number() over (order by id) - row_number() over (partition by session_id, message_name order by id)
                   ) as grp
            from logistics_meta_data_info t where extract (month FROM t.date) = extract (month FROM CURRENT_DATE)
           ) t
     ) t where message_name = 'MESSAGE_TO_SKILL') as t2 group by t2.new_id, t2.date) pg_aggregate

group by date order by date
"""
