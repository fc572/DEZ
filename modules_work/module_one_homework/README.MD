Question 1) 25.3
Question 2) postgres:5433
Question 3) 8007

        select count(*) from public.green_taxi_nov_2025
        where lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
        and trip_distance <= 1.00

Question 4) 2025-11-14

        SELECT lpep_pickup_datetime 
        FROM public.green_taxi_nov_2025 
        WHERE trip_distance = (SELECT MAX(trip_distance) FROM public.green_taxi_nov_2025 WHERE trip_distance <= 100.00);  

Question 5) East Harlem North

        select "PULocationID", sum(total_amount), zones."Zone"
        from public.green_taxi_nov_2025
        join zones on zones."LocationID" = public.green_taxi_nov_2025."PULocationID"
        where public.green_taxi_nov_2025.lpep_pickup_datetime between '2025-11-18 00:00:00' and '2025-11-18 23:59:59'
        GROUP BY "PULocationID", total_amount, zones."Zone"
        ORDER BY sum(total_amount) DESC

Question 6) Yorkville West

        SELECT "PULocationID", "DOLocationID", tip_amount, z1."Zone" as pickup_zone, z2."Zone" as dropoff_zone 
        FROM public.green_taxi_nov_2025
        JOIN zones z1 ON "PULocationID" = z1."LocationID"
        JOIN zones z2 ON "DOLocationID" = z2."LocationID"
        WHERE "PULocationID" = 74 
          AND lpep_pickup_datetime BETWEEN '2025-11-01 00:00:00' AND '2025-11-30 23:59:59'
        ORDER BY tip_amount DESC

Question 7) 