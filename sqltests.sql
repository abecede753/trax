select count(*) from tracks_track;

SELECT t.title, p.username, l.millis_per_km, l.millis, v.name, l.created
  FROM tracks_track t
     , tracks_laptime l
     , players_player p
     , vehicles_vehicle v
 WHERE l.track_id = t.id
   AND l.vehicle_id = v.id
   AND l.player_id = p.id
ORDER BY 6, 3
;




// dbext:type=pgsql:user=mawi:dbname=trax
