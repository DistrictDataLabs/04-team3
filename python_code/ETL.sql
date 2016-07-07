######To get home locations#####

Create TABLE IF NOT EXISTS home_loc(
unique_id TEXT,
home_lat TEXT,
home_lon TEXT,
num_people NUMERIC
);


INSERT INTO home_loc 
Select 
unique_id,
latitude,
longitude,
sal_1250_bel_jobs+sal_1250_3333_jobs+goods_prod_jobs+trade_transp_jobs+all_other_svc_jobs as num_people
FROM lodes_data where "TYPE"='Home' and latitude is not NULL AND longitude is not NULL;

######To get work locations######

Create TABLE IF NOT EXISTS work_loc(
unique_id TEXT,
work_lat TEXT,
work_lon TEXT 
);

INSERT INTO work_loc 
Select 
unique_id,
latitude,
longitude
FROM lodes_data where "type"= 'Work'
AND latitude is not null and longitude is not null;


######To get unique home and work locations#####


CREATE TABLE IF NOT EXISTS home_work(
home_lat TEXT,
home_lon TEXT ,
work_lat TEXT,
work_lon TEXT,
num_people NUMERIC 
);

INSERT INTO home_work 
Select 
home_lat,
home_lon,
work_lat,
work_lon,
sum(num_people)
FROM  home_loc inner join work_loc on home_loc.unique_id=work_loc.unique_id
group by 
home_lat,
home_lon,
work_lat,
work_lon;


#######Data filtering- Removing miles and min, converting ft to miles, hrs to min and s to min######

UPDATE car_info_hw
SET "distance.text" = CAST(CAST(RTRIM("distance.text", 'ft') AS INT)* 0.000189394 AS TEXT)
where "distance.text" LIKE '%ft%';

UPDATE car_info_hw
SET "distance.text" = RTRIM("distance.text", 'mi') 
where "distance.text" LIKE '%mi%';

UPDATE car_info_hw
SET "duration.text" = RTRIM("duration.text", 'mins')
where "duration.text" LIKE '%mins%';

UPDATE car_info_hw
SET "duration.text" = RTRIM("duration.text", 'min')
where "duration.text" LIKE '%min%';


#First check for minutes and then hours
UPDATE transit_info_hw
SET "duration.text" = RTRIM("duration.text", 'mins')
where "duration.text" LIKE '%mins%';

UPDATE transit_info_hw
SET "duration.text" = RTRIM("duration.text", 'min')
where "duration.text" LIKE '%min%';

UPDATE transit_info_hw
SET "duration.text" = cast(cast(substr( "duration.text", 1, instr( "duration.text", ' ' ) as INT)*60) as TEXT) 
where "duration.text" LIKE '%h%';

UPDATE transit_info_hw
SET "distance.text" = CAST(CAST(RTRIM("distance.text", 'ft') AS INT)* 0.000189394 AS TEXT)
where "distance.text" LIKE '%ft%';

UPDATE transit_info_hw
SET "distance.text" = RTRIM("distance.text", 'mi') 
where "distance.text" LIKE '%mi%';


#######Comparing car and transit data######
CREATE TABLE IF NOT EXISTS driving_data (
unique_id TEXT,
distance_in_miles DOUBLE,
duration_in_mins DOUBLE,
start_latitude DOUBLE,
start_longitude DOUBLE,
end_latitude DOUBLE,
end_longitude DOUBLE
);

INSERT INTO driving_data (unique_id,distance_in_miles, duration_in_mins, start_latitude, start_longitude, end_latitude, end_longitude)
Select 
unique_id,
cast("distance.text" AS DOUBLE),
CAST("duration.text" AS DOUBLE),
"start_location.lat",
"start_location.lng",
"end_location.lat",
"end_location.lng"
FROM  car_info_hw;

CREATE TABLE IF NOT EXISTS transit_data (
unique_id TEXT,
distance_in_miles DOUBLE,
duration_in_mins DOUBLE,
start_latitude DOUBLE,
start_longitude DOUBLE,
end_latitude DOUBLE,
end_longitude DOUBLE
);

INSERT INTO transit_data (unique_id,distance_in_miles, duration_in_mins, start_latitude, start_longitude, end_latitude, end_longitude)
Select 
unique_id,
cast("distance.text" AS DOUBLE),
CAST("duration.text" AS DOUBLE),
"start_location.lat",
"start_location.lng",
"end_location.lat",
"end_location.lng"
FROM  transit_info_hw
group by unique_id;

CREATE TABLE IF NOT EXISTS transit_compare (
unique_id TEXT,
transit_distance DOUBLE,
transit_duration DOUBLE,
car_distance DOUBLE,
car_duration DOUBLE,
car_transit_dur_diff DOUBLE,
start_latitude DOUBLE,
start_longitude DOUBLE,
end_latitude DOUBLE,
end_longitude DOUBLE,
class TEXT
);

INSERT INTO transit_compare (unique_id,transit_distance, transit_duration, car_distance, car_duration, car_transit_dur_diff, start_latitude, start_longitude ,end_latitude, end_longitude, class)
Select 
transit.unique_id,
transit."distance_in_miles" ,
transit."duration_in_mins",
car."distance_in_miles" ,
car."duration_in_mins",
abs(transit."duration_in_mins" - car."duration_in_mins"),
transit."start_latitude",
transit."start_longitude",
transit."end_latitude",
transit."end_longitude",
case when (transit."duration_in_mins" - car."duration_in_mins") > 30
THEN 'Poor transit'
ELSE
'Good transit'
END AS
FROM  transit_data transit INNER JOIN driving_data car
on transit.unique_id = car.unique_id;


######Walking miles >1######
CREATE TABLE IF NOT EXISTS transit_walk
(
unique_id TEXT,
travel_mode TEXT,
start_latitude DOUBLE,
start_longitude DOUBLE,
end_latitude DOUBLE,
end_longitude DOUBLE,
distance_in_miles DOUBLE,
duration_in_mins DOUBLE,
walk_class TEXT
);

INSERT INTO transit_walk (unique_id, travel_mode, start_latitude, start_longitude, end_latitude, end_longitude, distance_in_miles,duration_in_mins, walk_class)
SELECT
unique_id,
"travel_mode",
"start_location.lat",
"start_location.lng",
"end_location.lat",
"end_location.lng",
distance_in_miles,
duration_in_mins,
CASE WHEN distance_in_miles > 1
THEN "Poor transit"
ELSE
"Good transit"
END AS walk_class
FROM
(SELECT
unique_id,
"travel_mode",
"start_location.lat",
"start_location.lng",
"end_location.lat",
"end_location.lng",
sum("distance.text" ) as distance_in_miles,
sum("duration.text") as duration_in_mins,
NULL
FROM transit_steps_hw
where travel_mode LIKE '%WALKING%')
group By unique_id
order by distance_in_miles desc;



##############

CREATE TABLE IF NOT EXISTS buses_peak_time
(
TripHeadsign TEXT,
RouteID TEXT,
number_buses INT,
TripDirectionText TEXT,
directionNum TEXT
);

INSERT INTO buses_peak_time 
SELECT
TripHeadsign,
RouteID,
count(routeid),
TripDirectionText,
directionNum
from bus_schedules where endtime<'2016-06-13T10:00:00' and starttime>'2016-06-13T09:00:00' group By tripheadsign, routeid,DirectionNum , TripDirectionText;


CREATE TABLE IF NOT EXISTS min_buses
(
unique_id TEXT,
source_lat DOUBLE,
source_lon DOUBLE,
dest_lat DOUBLE,
dest_lon DOUBLE,
num_visits INT
min_bus_number INT,
routeid TEXT
);

INSERT INTO min_buses
SELECT
unique_id,
"start_location.lat",
"start_location.lng",
"end_location.lat",
"end_location.lng",
count("transit_details.departure_stop.location.lat") as num_visits,
min(schedules.number_buses),
schedules.routeid
FROM transit_steps_hw buses LEFT OUTER join  buses_peak_time schedules
on UPPER(buses."transit_details.headsign") = UPPER(schedules.TripHeadsign)
AND buses."transit_details.line.short_name" = schedules.routeid
where buses."transit_details.line.vehicle.type" = 'BUS' 
group BY unique_id;

CREATE TABLE IF NOT EXISTS transit_scarcity(
unique_id TEXT,
source_lat DOUBLE,
source_lon DOUBLE,
dest_lat DOUBLE,
dest_lon DOUBLE,
min_bus_number INT,
routeid TEXT,
num_people INT
)

INSERT INTO transit_scarcity
SELECT
unique_id,
source_lat,
source_lon ,
dest_lat,
dest_lon,
min_bus_number,
routeid,
num_people
FROM work_home num_people inner join  min_buses bus
people.home_lat = bus.source_lat and
people.home_lon = bus.source_lon and
people.work_lat = bus.source_lat and
people.work_lon = bus.source_lat
where min_bus_number*55 < (num_visits*num_people);










