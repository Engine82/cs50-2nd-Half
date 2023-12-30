-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Let's see what we have to work with
.tables
.schema crime_scene_reports


-- Per Specifiction the theft took place at 10:15am on July 28, 2021 on Humphrey Street


-- Find the corresponding crime scene report:
SELECT id, year, month, day, street FROM crime_scene_reports;


-- Pull the 2 reports on 2021-7-28 from Humphrey St
SELECT description
    FROM crime_scene_reports
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND street = 'Humphrey Street';


-- Look at interviews from that day
SELECT transcript FROM interviews
    WHERE year = 2021
    AND month = 7
    AND day = 28;


-- Thief make <1 min. phone call
-- Thief drove away within 10 min of theft  --- see security footage
-- Thief withdrew money from Leggett Street ATM before Eugene arrived at Emma's Bakery
-- Eugene recognized thief,

-- Thief planned to take earliest flight out of Fiftyville on 7-29-2021, and asked accomplice to purchase flight ticket


-- Look at phone calls <1 min to get an initial list of suspects
SELECT name FROM people
    WHERE phone_number IN(
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
    );

-- > Kenny, Sofia, Benista, Taylor, Diana, Kelsey, Bruce, Carina
-- Further filter by those who drove away from bakery on 7-28-2021

SELECT name FROM people
    WHERE phone_number IN(
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
    )
    AND license_plate IN(
        SELECT license_plate FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute > 15
        AND minute < 25
        AND activity = 'exit'
    );

-- > Sofia, Diana, Kelsey, Bruce

-- Find the time Eugene arrived at Emma's Bakery (before the theft)
SELECT hour, minute FROM bakery_security_logs
    WHERE license_plate IN(
        SELECT license_plate FROM people
        WHERE name = 'Eugene'
    )
    AND activity = 'entrance'
    AND hour < 11
    ORDER BY hour ASC;


-- Further filter by those who withdrew money from the Leggett St ATM on 7-28-2021, before 8:53:
-- See what the verbage is for withdrawals for next query
SELECT transaction_type FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28;

SELECT name FROM people
    WHERE phone_number IN(
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
    )
    AND license_plate IN(
        SELECT license_plate FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute > 15
        AND minute < 25
        AND activity = 'exit'
    )
    AND id IN(
        SELECT person_id FROM bank_accounts
        WHERE account_number IN(
            SELECT account_number FROM atm_transactions
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND atm_location = 'Leggett Street'
            AND transaction_type = 'withdraw'
        )
    );

-- > Diana and Bruce


-- Thief planned to take earliest flight out of Fiftyville on 7-29-2021, and asked accomplice to purchase flight ticket
SELECT name FROM people
    WHERE phone_number IN(
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
    )
    AND license_plate IN(
        SELECT license_plate FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute > 15
        AND minute < 25
        AND activity = 'exit'
    )
    AND id IN(
        SELECT person_id FROM bank_accounts
        WHERE account_number IN(
            SELECT account_number FROM atm_transactions
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND atm_location = 'Leggett Street'
            AND transaction_type = 'withdraw'
        )
    )
    AND passport_number IN(
        SELECT passport_number FROM passengers
        WHERE flight_id IN(
            SELECT id FROM flights
            WHERE year = 2021
            AND month = 7
            AND day = 29
            AND origin_airport_id IN(
                SELECT id FROM airports
                WHERE city = 'Fiftyville'
            )
            ORDER BY hour LIMIT 1
        )
    );

-- > Bruce is the thief!!!!


-- Now, to find the accomplice - see who Bruce called on the day of the theft for less than 1 minute.
SELECT name FROM people
    WHERE phone_number IN(
        SELECT receiver FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
        AND caller IN(
            SELECT phone_number FROM people
            WHERE name = 'Bruce'
        )
    );

-- > Robin is the accomplice!

-- Now, to find the city he flew to
SELECT city FROM airports
    WHERE id IN(
        SELECT destination_airport_id FROM flights
        WHERE id IN(
            SELECT flight_id FROM passengers
            WHERE passport_number IN(
                SELECT passport_number FROM people
                WHERE name = 'Bruce'
            )
        )
    );
-- > And Bruce flew to New York City!