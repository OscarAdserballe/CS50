-- Keep a log of any SQL queries you execute as you solve the mystery.

-- to get info of the crime
SELECT * FROM crime_scene_reports;
-- info from above query
-- Took place at 10:15am
-- At bakery
-- three witnesses interviewed who were present at the time

-- took place at 10:15 so only seems relevant to see what the logs picked up
SELECT * FROM bakery_security_logs WHERE year = 2021 AND day = 28 and hour = 10;
-- entrance at 10:08 R3G7486 -> Brandon
-- entrance at 10:14 with licence plate 13FNH73 -> Sophia
-- exit at 10:16 5P2BI95 -> Vanessa
-- exit at 10:18 94KL13X -> Bruce
-- exit at 10:18 6P58WS2 -> Barry
-- exit at 10:19 4328GD8 -> Luca

-- investigating people associated with those license plates:
SELECT name FROM people WHERE license_plate = "R3G7486";
-- etc. with all other license plates

--Seeing interviews
SELECT * FROM interviews WHERE year = 2021 AND day = 28 and month = 7;
-- Ruth stating thief entered car in parking lot within 10min
-- Eugene recognising the person from ATM earlier that morning
--  Raymond, thief leaving bakery called someone and talked for less than
-- a minute. Earliest flight out of Fiftyville. Thief asking accomplice to buy ticket
--

--Again... with new info
SELECT bakery_security_logs.hour, bakery_security_logs.minute, bakery_security_logs.license_plate, people.name FROM bakery_security_logs JOIN people ON people.license_plate = bakery_security_logs.license_plate WHERE year = 2021 AND day = 28 and hour = 10;
--From here, within 10:15 and 10:25 are the following suspects
-- Vanessa -> in list, 456 duration
-- Bruce -> in list, 45 duration, 120 duration, 241 duration, 75 duration
-- Barry -> in list, 583 duration
-- Luca
-- Sofia -> in list, 51 duration
-- Iman
-- Diana -> in list, 49 duration
-- Kelsey -> in list, 36 duration, 50 duration

--Calling while leaving:
SELECT people.name, phone_calls.duration FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller WHERE year = 2021 AND month = 7 AND day = 28 ORDER BY people.name;
--new suspect list
--Vanessa
--Bruce
--Barry
--Sofia
--Diana
--Kelsey

--at the bank earlier?
SELECT people.name, atm_transactions.atm_location, atm_transactions.transaction_type FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 ORDER BY people.name;
-- no help right now

--earliest flight
SELECT id, origin_airport_id, hour, minute, destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29;
-- earliest flight from 8:20 from 8 to 4 and flight_id 36

SELECT abbreviation, full_name FROM airports WHERE id = 8;
-- 8 is indeed Fiftyville, CSF

SELECT abbreviation, full_name FROM airports WHERE id = 4;
-- 4 is LaGuardia Airport, LGA

--passengers on flight id 36?
SELECT people.name FROM passengers JOIN people ON passengers.passport_number = people.passport_number JOIN flights ON flights.id = passengers.flight_id WHERE flight_id = 36 AND flights.year = 2021 AND flights.month = 7 AND flights.day = 29;
--Doris
--Sofia
--Bruce
--Edward
--Kelsey
--Taylor
--Kenny
--Luca

--cross-referencing with prev. lsit provides new list of suspects:
--Sofia -> not at atm
--Bruce -> At Leggett Street withdrawing
--Kelsey -> not at atm

--trying to crossreference list with this
SELECT people.name, atm_transactions.atm_location, atm_transactions.transaction_type FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 ORDER BY people.name;
-- Finally! Bruce is the thief!
--going to Laguardia from earlier command
--Accomplice?

--accomplice appearing on call sheet with bruce, 4 options
--buying ticket
--less than a minute

--phone number of Bruce:
SELECT phone_number, name FROM people WHERE name = "Bruce";
-- (367) 555-5533
SELECT people.name, phone_calls.duration FROM phone_calls JOIN people ON phone_calls.receiver = people.phone_number WHERE phone_calls.receiver = people.phone_number AND phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.caller = "(367) 555-5533";
--possible accomplices
--Robin -> 45 sec
--Deborah -> 120
--Gregory -> 241
--Carl -> 75

--Only Robin fits the description of a call less than a minute
-- -> Robin is the accomplice!

--city name where LaGuardia is
SELECT city FROM airports WHERE abbreviation = "LGA";
--New York City
