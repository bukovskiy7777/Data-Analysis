 with 
 raw_events as (
	 SELECT DISTINCT [session_id], page_group_id, event_datetime, [source], 
	 lag(page_group_id) over (PARTITION BY [test_dataset_DA].[session_id] ORDER BY [event_datetime] ) as prev_page_group_id
	 FROM [TrackingEvents].[dbo].[test_dataset_DA]
 ),

  filtered_raw_events as 
 (
	 SELECT [session_id], page_group_id, event_datetime, prev_page_group_id, [source],
	 ROW_NUMBER() OVER (PARTITION BY [session_id] ORDER BY event_datetime) as page_number
	 FROM raw_events
	 WHERE page_group_id!=prev_page_group_id OR prev_page_group_id is null
 ),

  session_landing_next_page as
(
	 SELECT [session_id], 
	 STRING_AGG(CAST(page_group_id as nvarchar(MAX)), ' -> ') WITHIN GROUP (ORDER BY event_datetime) AS landing_next_page_sequence
	 FROM  filtered_raw_events
	 WHERE page_number<3
	 GROUP BY [session_id]
),

session_first_page as
(
	 SELECT [session_id], [page_group_id] as landing_page
	 FROM  filtered_raw_events
	 WHERE page_number=1
), 

session_second_page as
(
	 SELECT [session_id], [page_group_id] as next_page
	 FROM  filtered_raw_events
	 WHERE page_number=2
),

  session_page_sequence as 
(
	  SELECT [session_id], MIN(event_datetime) as session_start, [source], 
	  STRING_AGG(CAST(page_group_id as nvarchar(MAX)), ' -> ') WITHIN GROUP (ORDER BY event_datetime) AS page_sequence,
	  MAX(page_number) as session_length
	  FROM  filtered_raw_events
	  GROUP BY [session_id], [source]

),

  session_add_to_cart as 
(
	SELECT DISTINCT [session_id], 1 as add_to_cart
	FROM [TrackingEvents].[dbo].[test_dataset_DA]
	WHERE [event_type]=6
),

  session_create_order as 
(
	SELECT DISTINCT [session_id], 1 as create_order
	FROM [TrackingEvents].[dbo].[test_dataset_DA]
	WHERE [event_type]=8

)

	SELECT [source], session_start, session_page_sequence.[session_id], page_sequence, session_length, landing_next_page_sequence,
	landing_page, next_page, session_add_to_cart.add_to_cart, session_create_order.create_order
	FROM  session_page_sequence
	LEFT JOIN session_landing_next_page on session_page_sequence.session_id=session_landing_next_page.session_id
	LEFT JOIN session_add_to_cart on session_page_sequence.session_id=session_add_to_cart.session_id
	LEFT JOIN session_create_order on session_page_sequence.session_id=session_create_order.session_id
	LEFT JOIN session_first_page on session_page_sequence.session_id=session_first_page.session_id
	LEFT JOIN session_second_page on session_page_sequence.session_id=session_second_page.session_id
;
  



