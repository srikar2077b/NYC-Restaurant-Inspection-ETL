-- Description: Cleans and inserts data from raw table into cleaned table

CREATE OR ALTER PROCEDURE CleanRestaurantInspectionData
AS
BEGIN
    SET NOCOUNT ON;

    TRUNCATE TABLE Cleaned_RestaurantData;

    INSERT INTO Cleaned_RestaurantData
    SELECT
        RES_ID,
        RES_NAME,
        UPPER(BORO),
        CASE WHEN BUILDING IS NULL OR BUILDING IN ('NA', 'NaN', 'nan', '') THEN 'UNKNOWN' ELSE BUILDING END,
        TRIM(REPLACE(REPLACE(REPLACE(STREET, '  ', ' '), '\t', ''), '\n', '')),
        CASE WHEN ZIPCODE IS NULL OR ZIPCODE IN ('0', 'NA', 'NaN', 'nan', '') THEN '00000' ELSE ZIPCODE END,
        PHONE_NUMBER,
        CUISINE_DESCRIPTION,
        INSPECTION_DATE,
        ACTION,
        VIOLATION_CODE,
        VIOLATION_DESCRIPTION,
        CASE WHEN CRITICAL_FLAG = 'Not Applicable' THEN 'Not Critical' ELSE CRITICAL_FLAG END,
        ISNULL(SCORE, 0),
        GRADE,
        RECORD_DATE,
        INSPECTION_TYPE,
        INSPECTION_YEAR,
        INSPECTION_MONTH,
        INSPECTION_DAY,
        INSPECTION_WEEK_NUMBER,
        RISK_CATEGORY,
        TRIM(REPLACE(REPLACE(REPLACE(FULL_ADDRESS, '  ', ' '), '\t', ''), '\n', ''))
    FROM Inspected_RestaurantData;

END;