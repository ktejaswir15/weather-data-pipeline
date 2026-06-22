-- Final mart model: analytics-ready weather summary
SELECT
    CITY,
    COUNTRY,
    TEMPERATURE,
    TEMPERATURE_F,
    TEMP_CATEGORY,
    FEELS_LIKE,
    HUMIDITY,
    WIND_SPEED,
    WEATHER_DESC,
    EXTRACTED_AT,
    -- Comfort index (combining temp and humidity)
    CASE
        WHEN HUMIDITY > 80 AND TEMPERATURE > 25 THEN 'Very Uncomfortable'
        WHEN HUMIDITY > 60 AND TEMPERATURE > 20 THEN 'Uncomfortable'
        WHEN HUMIDITY < 40 AND TEMPERATURE BETWEEN 15 AND 25 THEN 'Very Comfortable'
        ELSE 'Comfortable'
    END AS COMFORT_INDEX,
    -- Wind description
    CASE
        WHEN WIND_SPEED < 5  THEN 'Calm'
        WHEN WIND_SPEED < 15 THEN 'Breezy'
        WHEN WIND_SPEED < 30 THEN 'Windy'
        ELSE 'Very Windy'
    END AS WIND_CATEGORY
FROM {{ ref('stg_weather') }}
