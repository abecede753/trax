select count(*) from players_player;

-- user,vehicle,track
SELECT p.username
   , p.id AS player_id
   , t.title
   , t.id AS track_id
   , v.name
   , v.id AS vehicle_id
   , min(l.millis_per_km) AS minmillis
   , max(l.millis_per_km) AS maxmillis
--   , median(l.millis_per_km) AS medianmillis
   , count(*) AS num_entries
   , 100 AS weight
FROM players_player p
   , tracks_track t
   , tracks_laptime l
   , vehicles_vehicle v
WHERE l.player_id = p.id
  AND l.track_id = t.id
  AND l.vehicle_id = v.id
GROUP BY p.username, p.id, t.title, t.id, v.name, v.id
ORDER BY 9 DESC, 7 ASC

-- median of (user,vehicle), (vehicle,track)

-- user,vehicle IF > 2

-- vehicle,track IF > 2

-- user (factor to cc_millis) IF more than 5 laptimes found

-- cc_millis

-- dbext:type=PGSQL:user=trax
