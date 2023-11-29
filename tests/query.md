# NoQ Data

SQL

## Reservation och User

SELECT * FROM reservation inner join users where users.id = reservation.user_id

## Reservation brukare, startdatum och härbärge

SELECT users.name as "Brukare", reservation.start_date as "Datum", hosts.name as "Härbärge", reservation.updated_at as "Uppdaterad"
FROM reservation
INNER JOIN users ON reservation.user_id = users.id
INNER JOIN hosts ON reservation.host_id = hosts.id
order by users.name, start_date;
