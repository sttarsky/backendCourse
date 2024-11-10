Заезд '2024-11-01'
выезд '2024-12-14'

select *
from bookings;


select *
from bookings
where date_from <= '2024-12-14' and date_to >= '2024-11-01';

# %%%%%% считаем количество занятых комнат за период

select bookings.room_id, count(*)
from bookings
where date_from <= '2024-12-14' and date_to >= '2024-11-01'
group by room_id;

# %%%%%% получаем id комнаты и сколько их осталось

with rooms_booked as (
	select bookings.room_id, count(*) as booked
	from bookings
	where date_from <= '2024-11-30' and date_to >= '2024-11-01'
	group by room_id
),
rooms_purches as (
select rooms.id as room_id,  quantity - coalesce(booked, 0) as rooms_left
from rooms 
left join rooms_booked
on rooms_booked.room_id = rooms.id
)
select *
from rooms_purches
where rooms_left > 0  and room_id in (select rooms.id from rooms );

# %%%%%% получаем все свободные номера

select *
from rooms
where rooms.id in (
with rooms_booked as (
	select bookings.room_id, count(*) as booked
	from bookings
	where date_from <= '2024-11-30' and date_to >= '2024-10-01'
	group by room_id
),
rooms_purches as (
select rooms.id as room_id,  quantity - coalesce(booked, 0) as rooms_left
from rooms 
left join rooms_booked
on rooms_booked.room_id = rooms.id
)
select rooms_purches.room_id
from rooms_purches
where rooms_left > 0  and room_id in (select rooms.id from rooms where rooms.hotel_id = 16)
);

# %%%%% получаем все отели с свободными номерами

select *
from hotels
where hotels.id in (
select rooms.hotel_id 
from rooms
where rooms.id in (
with rooms_booked as (
	select bookings.room_id, count(*) as booked
	from bookings
	where date_from <= '2026-11-30' and date_to >= '2026-11-01'
	group by room_id
),
rooms_purches as (
select rooms.id as room_id,  quantity - coalesce(booked, 0) as rooms_left
from rooms 
left join rooms_booked
on rooms_booked.room_id = rooms.id
)
select rooms_purches.room_id
from rooms_purches
where rooms_left > 0  and room_id in (select rooms.id from rooms)
));


