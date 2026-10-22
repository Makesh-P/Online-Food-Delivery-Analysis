import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine(
    f"mysql+pymysql://root:makesh28@localhost:3306/online_food_delivery_db"
)


query = """select Customer_ID ,
                sum(Final_Amount) AS total,
                Count(*) as Count 
            from orders
            where Order_Status = "Delivered"
            group by Customer_ID
            order by total DESC
            LIMIT 10;"""
result = pd.read_sql(query, engine)
print("1\n",result)

query = """select Customer_Segment, 
            round(avg(Order_Value),2)as Avg_order_value,
            count(*) as No_order
            from orders
        where Order_Status = "Delivered"
        group by Customer_Segment
        order by Avg_order_value DESC;"""
result = pd.read_sql(query, engine)
print("2\n",result)

query = """SELECT Order_Day,
              COUNT(*) AS Orders,
              COUNT(DISTINCT Order_Date) AS Days_In_Data,
              ROUND(COUNT(*) / COUNT(DISTINCT Order_Date), 1) AS Orders_Per_Day
       FROM orders
       where Order_Status = "Delivered"
       GROUP BY Order_Day;"""
result = pd.read_sql(query,engine)
print("3\n",result)


query = """select 
                month(Order_Date) as Month , 
                Count(*) as Orders ,
                round(sum(Final_Amount),2) as Revenue
            from orders
            where Order_Status ="Delivered"
            group by Month
            order by Month;"""
result = pd.read_sql(query,engine)
print("4\n",result)


query = """SELECT CASE
                WHEN Discount_Applied = 0 THEN 'No Discount'
                ELSE 'Discount'
              END AS Discount_Status,
              COUNT(*) AS Orders,
              ROUND(AVG(Profit_Margin), 2) AS Avg_Profit_Margin
            FROM orders
            WHERE Order_Status = 'Delivered'
            GROUP BY Discount_Status;"""
result = pd.read_sql(query,engine)
print("5\n",result)

query = """Select City , 
                Cuisine_Type,
                Sum(Final_Amount) as Revenue
            from orders
            where Order_Status = "Delivered"
            group by City, Cuisine_Type
            order by Revenue DESC;"""
result = pd.read_sql(query, engine)
print("6\n",result)


query = """SELECT City , 
                Count(*) as Orders,
                round(avg(Delivery_Time_Min),2) as Avg_Delivery_Time
            from orders
            where Order_Status = "Delivered"
            group by City;"""
result = pd.read_sql(query, engine)
print("7\n",result)

query = """SELECT CASE
                  WHEN Distance_km <= 10 THEN '1. Up to 10 km'
                  WHEN Distance_km <= 20 THEN '2. 10-20 km'
                  WHEN Distance_km <= 30 THEN '3. 20-30 km'
                  ELSE '4. Above 30 km'
              END AS Distance_Band,
              COUNT(*) AS Orders,
              ROUND(AVG(Delivery_Time_Min), 1) AS Avg_Delivery_Time,
              ROUND(100 * AVG(Delivery_Time_Min > 120), 1) AS Percentage
       FROM orders
       WHERE Order_Status = 'Delivered'
       GROUP BY Distance_Band
       ORDER BY Distance_Band;"""
result = pd.read_sql(query, engine)
print("8\n",result)

query= """SELECT 
                Delivery_Rating , 
                round(avg(Delivery_Time_Min),2) as Avg_Delivery_Time
                from orders
            where Order_Status = "Delivered"
            group by Delivery_Rating
            order by Delivery_Rating;"""
result = pd.read_sql(query, engine)
print("9\n",result)

query = """SELECT 
                Restaurant_Name ,
                round(avg(Restaurant_Rating),2) as Avg_Restaurant_Rating,
                Count(*) as Orders
                from orders
            group by Restaurant_Name
            order by Avg_Restaurant_Rating DESC,Orders DESC
            Limit 10;"""
result = pd.read_sql(query,engine)
print("10\n",result)


query = """SELECT
                Restaurant_Name , 
                count(*) as Orders,
                sum(Order_Status = "Cancelled") as Cancelled,
                round(100 * avg(Order_Status = "Cancelled"),2) as Cancellation_rate
            from orders 
            group by Restaurant_Name
            order by Cancellation_rate DESC
            Limit 10;"""
result = pd.read_sql(query,engine)
print("11\n",result)


query = """SELECT 
                Cuisine_Type ,
                Count(*) as Orders,
                round(sum(Final_Amount),2) as Revenue,
                round(avg(Restaurant_Rating),2) as Avg_Restaurant_Rating,
                round(avg(Profit_Margin),2) as Avg_Profit_Margin
            from orders
            where Order_Status = "Delivered"
            group by Cuisine_Type
            order by Revenue DESC;"""
result = pd.read_sql(query,engine)
print("12\n",result)

query = """SELECT 
                Peak_Hour,
                count(*) as Orders,
                round(avg(Final_Amount),2) as Avg_Revenue,
                round(avg(Delivery_Time_Min),2) as Avg_Delivery_Time_Min
            from orders
            where Order_Status = "Delivered"
            group by Peak_Hour
            order by Orders DESC;"""
result = pd.read_sql(query, engine)
print("13\n",result)


query = """SELECT 
                Payment_Mode , 
                Count(*) as Orders ,
                RANK() over(order by count(*) DESC) as Priority
            from orders
            group by Payment_Mode
            order by Priority"""
result = pd.read_sql(query, engine)
print("14\n",result)

query = """SELECT 
                Cancellation_Reason,
                Count(*) as Orders,
                RANK() over(order by count(*) DESC) AS Priority
            from orders
            WHERE Order_Status = "Cancelled"
            group by Cancellation_Reason
            order by Priority"""
result = pd.read_sql(query, engine)
print("15\n",result)