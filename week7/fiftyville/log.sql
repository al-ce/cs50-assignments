-- Keep a log of any SQL queries you execute as you solve the mystery.

/*
CREATE TABLE crime_scene_reports (
    id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    street TEXT,
    description TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE interviews (
    id INTEGER,
    name TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    transcript TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE atm_transactions (
    id INTEGER,
    account_number INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    atm_location TEXT,
    transaction_type TEXT,
    amount INTEGER,
    PRIMARY KEY(id)
);
CREATE TABLE bank_accounts (
    account_number INTEGER,
    person_id INTEGER,
    creation_year INTEGER,
    FOREIGN KEY(person_id) REFERENCES people(id)
);
CREATE TABLE airports (
    id INTEGER,
    abbreviation TEXT,
    full_name TEXT,
    city TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE flights (
    id INTEGER,
    origin_airport_id INTEGER,
    destination_airport_id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    minute INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(origin_airport_id) REFERENCES airports(id),
    FOREIGN KEY(destination_airport_id) REFERENCES airports(id)
);
CREATE TABLE passengers (
    flight_id INTEGER,
    passport_number INTEGER,
    seat TEXT,
    FOREIGN KEY(flight_id) REFERENCES flights(id)
);
CREATE TABLE phone_calls (
    id INTEGER,
    caller TEXT,
    receiver TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    duration INTEGER,
    PRIMARY KEY(id)
);
CREATE TABLE people (
    id INTEGER,
    name TEXT,
    phone_number TEXT,
    passport_number INTEGER,
    license_plate TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE bakery_security_logs (
    id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    minute INTEGER,
    activity TEXT,
    license_plate TEXT,
    PRIMARY KEY(id)
);
*/

-- NOTE: 00 List of suspects


-- NOTE: 01
-- Query crime_scene_reports table for all information on the day
-- and location of the theft of the duck.
SELECT description, id
  FROM crime_scene_reports
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND street = "Humphrey Street"
;


-- Output:
-- | id    | 295 |
-- | description |
-- | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- | Interviews were conducted today with three witnesses who were present at
-- | the time – each of their interview transcripts mentions the bakery. |


-- NOTE: 02
-- Query interviews on day of theft, as suggested by theft report.
SELECT name, transcript
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
;

-- Relevant Output (transcripts that mention the bakery, per theft report)
-- +---------+-----------------------------------------------------------------
-- | name    | transcript                                                                                                                                                                                                                                                                                                          |
-- +---------+-----------------------------------------------------------------
-- | Ruth    | Sometime within ten minutes of the theft, I saw the thief get
-- |         | into a car in the bakery parking lot and drive away. If you have
-- |         | security footage from the bakery parking lot, you might want to
-- |         | look for cars that left the parking lot in that time frame.
-- +---------+-----------------------------------------------------------------
-- | Eugene  | I dont know the thiefs name, but it was someone I recognized.
-- |         | Earlier this morning, before I arrived at Emmas bakery, I was
-- |         | walking by the ATM on Leggett Street and saw the thief there
-- |         | withdrawing some money.
-- +---------+-----------------------------------------------------------------
-- | Raymond | As the thief was leaving the bakery, they called someone who
-- |         | talked to them for less than a minute. In the call, I heard the
-- |         | thief say that they were planning to take the earliest flight
-- |         | out of Fiftyville tomorrow. The thief then asked the person on
-- |         | the other end of the phone to purchase the flight ticket.
-- +---------+-----------------------------------------------------------------

-- From Ruth:
--  Check bakery_security_logs for car that exited the parking lot between
--  10:15am and 10:25am on the day of the theft.
-- From Eugene:
--  Check atm_transcations for withdrawls on Legget on the day of the theft.
-- From Raymond:
--  Check phone_calls for calls around 10:15am with <1m duration.
--  Caller is thief, recipient is accomplice, so mark both on suspects list.
--  Check flights for earliest flight out of Fiftyville on 29 Jul 2021.


-- NOTE: 03
--  Check bakery_security_logs for car that exited the parking lot between
--  10:15am and 10:25am on the day of the theft.
-- (cf Note 02)

SELECT activity, bsl.license_plate, name
  FROM bakery_security_logs AS bsl
       JOIN people
            ON people.license_plate = bsl.license_plate
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND hour = 10
   AND minute BETWEEN 15 and 25
;


-- Output
-- TODO: EVIDENCE: one of these cars belongs to the thief.
-- +----------+---------------+---------+
-- | activity | license_plate | name    |
-- +----------+---------------+---------+
-- | exit     | 5P2BI95       | Vanessa |
-- | exit     | 94KL13X       | Bruce   |
-- | exit     | 6P58WS2       | Barry   |
-- | exit     | 4328GD8       | Luca    |
-- | exit     | G412CB7       | Sofia   |
-- | exit     | L93JTIZ       | Iman    |
-- | exit     | 322W7JE       | Diana   |
-- | exit     | 0NTHK55       | Kelsey  |
-- +----------+---------------+---------+


-- NOTE: 04
--  Check atm_transcations for withdrawls on Legget on the day of the theft.
-- (cf Note 02)

SELECT atm_transactions.account_number, transaction_type, people.name
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
;

-- Output:
-- TODO: EVIDENCE: One of these names belongs to the thief.
-- TODO: EVIDENCE: The account the thief withdrew from could belong to the thief or the accomplice.
-- +----------------+------------------+---------+
-- | account_number | transaction_type | name    |
-- +----------------+------------------+---------+
-- | 49610011       | withdraw         | Bruce   |
-- | 26013199       | withdraw         | Diana   |
-- | 16153065       | withdraw         | Brooke  |
-- | 28296815       | withdraw         | Kenny   |
-- | 25506511       | withdraw         | Iman    |
-- | 28500762       | withdraw         | Luca    |
-- | 76054385       | withdraw         | Taylor  |
-- | 81061156       | withdraw         | Benista |
-- +----------------+------------------+---------+


-- NOTE: 05
--  Check phone_calls for calls around 10:15am with <1m duration.
--  Caller is thief, recipient is accomplice, so mark both on suspects list.
-- (cf Note 02)

SELECT phone.caller, p1.name, phone.receiver, p2.name
  FROM phone_calls AS phone
       JOIN people AS p1
            ON phone.caller = p1.phone_number
       JOIN people AS p2
            ON phone.receiver = p2.phone_number
  WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
;

-- TODO: EVIDENCE: A Caller is the thief, a reciever is the accomplice.
-- +----------------+---------+----------------+------------+
-- | caller         | name    | receiver       | name       |
-- +----------------+---------+----------------+------------+
-- | (130) 555-0289 | Sofia   | (996) 555-8899 | Jack       |
-- | (499) 555-9472 | Kelsey  | (892) 555-8872 | Larry      |
-- | (367) 555-5533 | Bruce   | (375) 555-8161 | Robin      |
-- | (499) 555-9472 | Kelsey  | (717) 555-1342 | Melissa    |
-- | (286) 555-6063 | Taylor  | (676) 555-6554 | James      |
-- | (770) 555-1861 | Diana   | (725) 555-3243 | Philip     |
-- | (031) 555-6622 | Carina  | (910) 555-3251 | Jacqueline |
-- | (826) 555-1652 | Kenny   | (066) 555-9701 | Doris      |
-- | (338) 555-6650 | Benista | (704) 555-2131 | Anna       |
-- +----------------+---------+----------------+------------+


-- NOTE 06:
--  Check flights for earliest flight out of Fiftyville on 29 Jul 2021.

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
 ORDER BY hour, minute, seat;

-- +--------+------------+------+------------+---------------+----+------+-------+-----+------+--------+
-- | name   | passport   | seat | origin     | destination   | id | year | month | day | hour | minute |
-- +--------+------------+------+------------+---------------+----+------+-------+-----+------+--------+
-- | Doris  | 7214083635 | 2A   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Sofia  | 1695452385 | 3B   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Bruce  | 5773159633 | 4A   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Edward | 1540955065 | 5C   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Kelsey | 8294398571 | 6C   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Taylor | 1988161715 | 6D   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Kenny  | 9878712108 | 7A   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- | Luca   | 8496433585 | 7B   | Fiftyville | New York City | 36 | 2021 | 7     | 29  | 8    | 20     |
-- +--------+------------+------+------------+---------------+----+------+-------+-----+------+--------+

-- NOTE: 07
-- Cross reference all previous queries to get thief and accomplice names
-- based on information gathered from three bystanders on the day of the theft.

SELECT p1.name AS suspected_thief, p2.name AS suspected_accomplice
  FROM phone_calls AS phone
       JOIN people AS p1
            ON phone.caller = p1.phone_number
       JOIN people AS p2
            ON phone.receiver = p2.phone_number
  WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
    AND p1.name IN
    (
-- Get thiefs name
SELECT name
  FROM people
       JOIN passengers as pass
            ON people.passport_number = pass.passport_number
       JOIN flights AS f
            ON pass.flight_id = f.id
       JOIN airports AS o
            ON f.origin_airport_id = o.id
       JOIN airports AS d
            ON f.destination_airport_id = d.id
 WHERE year = 2021             -- Limit to flights on 29/7/21 (cf Raymonds interview, Note 02)
   AND month = 7
   AND day = 29
   AND o.city = "Fiftyville"
   AND f.id IN                 -- Get the _earliest_ flight out
       (SELECT id
          FROM flights
          WHERE year = 2021
            AND month = 7
            AND day = 29
          ORDER BY hour, minute
          LIMIT 1)
   AND name IN                 -- Limit names to those that made a phone call
       (                       -- on day of theft that lasted less than 60 sec
       SELECT p1.name          -- (cf Raymond's interview, Note 02)
         FROM phone_calls AS phone
              JOIN people AS p1
                   ON phone.caller = p1.phone_number
         WHERE year = 2021
           AND month = 7
           AND day = 28
           AND duration < 60
       )
   AND name IN                 -- Limit names to those that made a withdrawl
       (                       -- on Legget Street on day of the theft
       SELECT name             -- (cf Eugene's interview, Note 02)
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
   AND name IN                 -- Limit names to those whose car was seen
        (                      -- driving away within 10m of theft (cf Ruth's interview)
        SELECT name
          FROM bakery_security_logs as bsl
               JOIN people
                    ON people.license_plate = bsl.license_plate
         WHERE year = 2021
           AND month = 7
           AND day = 28
           AND hour = 10
           AND minute BETWEEN 15 and 25
        )
    );
