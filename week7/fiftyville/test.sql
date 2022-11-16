SELECT name,
       people.passport_number AS passport,
       seat,
       o.city AS origin,
       d.city AS destination,
       f.id,
       f.year, f.month, f.day, f.hour, f.minute
  FROM people
       JOIN passengers as pass
            ON people.passport_number = pass.passport_number
       JOIN flights AS f
            ON pass.flight_id = f.id
       JOIN airports AS o
            ON f.origin_airport_id = o.id
       JOIN airports AS d
            ON f.destination_airport_id = d.id
 WHERE year = 2021
   AND month = 7
   AND day = 29
   AND o.city = "Fiftyville"
   AND f.id IN
       (SELECT id
          FROM flights
          WHERE year = 2021
            AND month = 7
            AND day = 29
          ORDER BY hour, minute
          LIMIT 1)
   AND name IN
       (
       SELECT p1.name
         FROM phone_calls AS phone
              JOIN people AS p1
                   ON phone.caller = p1.phone_number
         WHERE year = 2021
           AND month = 7
           AND day = 28
           AND duration < 60
       )

+--------+------------+------+------------+---------------+----+------+-------+-----+------+--------+
| name   | passport   | seat | origin     | destination   | id | year | month | day | hour | minute |
+--------+------------+------+------------+---------------+----+------+-------+-----+------+--------+
| Sofia  | 1695452385 | 3B   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
| Bruce  | 5773159633 | 4A   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
| Kelsey | 8294398571 | 6C   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
| Taylor | 1988161715 | 6D   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
| Kenny  | 9878712108 | 7A   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
+--------+------------+------+------------+---------------+----+------+-------+-----+------+--------+



SELECT name,
       people.passport_number AS passport,
       seat,
       o.city AS origin,
       d.city AS destination,
       f.id,
       f.year, f.month, f.day, f.hour, f.minute
  FROM people
       JOIN passengers as pass
            ON people.passport_number = pass.passport_number
       JOIN flights AS f
            ON pass.flight_id = f.id
       JOIN airports AS o
            ON f.origin_airport_id = o.id
       JOIN airports AS d
            ON f.destination_airport_id = d.id
 WHERE year = 2021
   AND month = 7
   AND day = 29
   AND o.city = "Fiftyville"
   AND f.id IN
       (SELECT id
          FROM flights
          WHERE year = 2021
            AND month = 7
            AND day = 29
          ORDER BY hour, minute
          LIMIT 1)
   AND name IN
       (
       SELECT p1.name
         FROM phone_calls AS phone
              JOIN people AS p1
                   ON phone.caller = p1.phone_number
         WHERE year = 2021
           AND month = 7
           AND day = 28
           AND duration < 60
       )
   AND name IN
       (
       SELECT name
         FROM atm_transactions
              JOIN bank_accounts
                ON atm_transactions.account_number = bank_accounts.account_number
              JOIN people
                ON bank_accounts.person_id = people.id
        WHERE year = 2021
          AND month = 7
          AND day = 28
          AND atm_location = "Leggett Street"
          AND transaction_type = "withdraw"
        )
   AND name IN
        (
        SELECT name
          FROM bakery_security_logs
               JOIN people
                    ON people.license_plate = bsl.license_plate
         WHERE year = 2021
           AND month = 7
           AND day = 28
           AND hour = 10
           AND minute BETWEEN 15 and 25
        )
;
