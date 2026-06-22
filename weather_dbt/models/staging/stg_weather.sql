-- Staging model: clean and cast raw weather data
SELECT
    CITY,
    COUNTRY,
    TEMPERATURE,
    FEELS_LIKE,
    HUMIDITY,
    WEATHER_DESC,
    WIND_SPEED,
    EXTRACTED_AT,
    -- Add temperature in Fahrenheit
    ROUND((TEMPERATURE * 9/5) + 32, 1) AS TEMPERATURE_F,
    -- Categorize temperature
    CASE
        WHEN TEMPERATURE < 0  THEN 'Freezing'
        WHEN TEMPERATURE < 10 THEN 'Cold'
        WHEN TEMPERATURE < 20 THEN 'Mild'
        WHEN TEMPERATURE < 30 THEN 'Warm'
        ELSE 'Hot'
    END AS TEMP_CATEGORY
FROM {{ source('raw', 'WEATHER_RAW') }}