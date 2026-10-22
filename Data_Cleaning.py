import pandas as pd
import numpy as np

# Load Dataset
df = pd.read_csv(r"C:\Data science and gen AI\Practice\Project_2\ONINE_FOOD_DELIVERY_ANALYSIS.csv") # Change the path
df.head()

# Data Inspection
df.isnull().sum()
df.dtypes

# Separate Numerical and Categorical Columns
num_col = df.select_dtypes(include=['int64', 'float64']).columns
num_col

cat_col = df.select_dtypes(include=['object']).columns
cat_col

# Convert Order Date to Datetime Format
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%m/%d/%Y")

# Analyze Missing Values
null_check = df.isnull().sum()
null_num = null_check[num_col]
print(null_num)

null_cat = null_check[cat_col]
print(null_cat)

df.isnull().mean() * 100

# Data Cleaning and Missing Value Imputation
df_1 = df.copy()

# Fill Missing Categorical Values Using Mode
categorical_columns = ["City", "Area", "Cuisine_Type", "Payment_Mode", "Customer_Gender"]
for i in categorical_columns:
    df_1[i] = df_1[i].fillna(df_1[i].mode()[0])

# Fill Missing Numerical Values Using Median
numerical_columns = ["Discount_Applied", "Delivery_Rating"]
for i in numerical_columns:
    df_1[i] = df_1[i].fillna(df_1[i].median())

df_1["Order_Value"] = df_1["Order_Value"].fillna(df_1["Order_Value"].median())
df_1["Distance_km"] = df_1["Distance_km"].fillna(df_1["Distance_km"].median())

# Handle Missing Values and Outliers in Delivery Time
cap = df_1["Delivery_Time_Min"].quantile(0.95)
df_1["Delivery_Time_Min"] = df_1["Delivery_Time_Min"].fillna(df_1["Delivery_Time_Min"].median())
df_1["Delivery_Time_Min"] = df_1["Delivery_Time_Min"].clip(upper=cap)

# Calculate Final Amount After Applying Discount
df_1["Discount_Applied"] = np.minimum(df_1["Discount_Applied"], df_1["Order_Value"])
df_1["Final_Amount"] = df_1["Order_Value"] - df_1["Discount_Applied"]

# Remove Rows with Missing Order Dates
df_1["Order_Date"] = pd.to_datetime(df_1["Order_Date"], format="%m/%d/%Y")
df_1 = df_1.dropna(subset=["Order_Date"]).reset_index(drop=True)
df_1 = df_1.drop(columns="Order_Time")

# Fill Missing Customer Ages Using City-wise Median
df_1["Customer_Age"] = df_1["Customer_Age"].fillna(
    df_1.groupby("City")["Customer_Age"].transform("median")
).astype(int)

# Handle Missing Cancellation Reasons
df_1.loc[df_1["Order_Status"] == "Delivered", "Cancellation_Reason"] = "Not Applicable"
df_1["Cancellation_Reason"] = df_1["Cancellation_Reason"].fillna("Not Specified")

# Standardize Peak Hour Values
df_1["Peak_Hour"] = df_1["Peak_Hour"].map({True: "Peak", False: "Off-Peak"}).fillna("Unknown")

# Keep Restaurant Ratings Within the Valid Range
df_1["Restaurant_Rating"] = df_1["Restaurant_Rating"].clip(upper=5)

# Validate Cleaned Data
df_1.isnull().mean() * 100
df_1.duplicated().sum()
df_1.dtypes

# Remove Records with Negative Profit Margins
df_1 = df_1[df_1["Profit_Margin"] >= 0].reset_index(drop=True)

# Standardize Categorical Text Values
cat_col_std = [
    'Customer_Gender', 'City', 'Area',
    'Restaurant_Name', 'Cuisine_Type',
    'Order_Status', 'Cancellation_Reason',
    'Order_Day', 'Peak_Hour'
]

for c in cat_col_std:
    df_1[c] = df_1[c].str.strip().str.title()

# Generate Descriptive Statistics
df_1.describe()

# Feature Engineering

# Categorize Delivery Time
def delivery_category(time):
    if time <= 60:
        return "Quick"
    elif time <= 120:
        return "Normal"
    else:
        return "Delayed"

df_1["Delivery_Category"] = df_1["Delivery_Time_Min"].apply(delivery_category)

# Segment Customers by Age
def age_category(age):
    if age < 30:
        return "Young"
    elif age < 45:
        return "Adult"
    else:
        return "Senior"

df_1["Customer_Segment"] = df_1["Customer_Age"].apply(age_category)

df_1.head()

# Create MySQL Database
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="makesh28"
)

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS online_food_delivery_db")
cursor.close()
connection.close()

print("Database created successfully")

# Connect to MySQL with the cleaned dataset
from sqlalchemy import create_engine

engine = create_engine(
    f"mysql+pymysql://root:makesh28@localhost:3306/online_food_delivery_db"
)

df_1.to_sql(
    "orders",
    con=engine,
    if_exists="replace",
    index=False
)

print("Table created and data inserted successfully")