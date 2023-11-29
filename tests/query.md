# Reservation och User

SELECT * FROM reservation inner join users where users.id = reservation.user_id

# Reservation startdatum, namn och härbärge
SELECT Date(reservation.startDateTime) as Datum, users.name as Brukare, hosts.name as "Härbärge"
FROM reservation
INNER JOIN users ON reservation.user_id = users.id
INNER JOIN hosts ON reservation.host_id = hosts.id;