import csv              # to read and write CSV files
from datetime import datetime   # to work with dates


import pandas as pd     # for data analysis
import matplotlib.pyplot as plt  # for charts

FileName= "groceries.csv"

def add_item():

    name = input("Enter item name: ")
    purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
    quantity = input("Enter quantity: ")

    with open("groceries.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, purchase_date, expiry_date, quantity, "Fresh"])

    print("Item added successfully!\n")

def list_items():
    with open("groceries.csv", "r") as file:
        reader = csv.reader(file)
        print("\n All Grocery Items:")
        for row in reader:
            print(row)
    print()

def check_expiry():
    today = datetime.today()
    rows = []

    with open("groceries.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Save header 
        for row in reader:
            if row:  # skip empty rows
                expiry_date = datetime.strptime(row[2], "%Y-%m-%d")
                days_left = (expiry_date - today).days

                # Update status based on expiry
                if days_left < 0:
                    row[4] = "Expired"
                elif days_left <= 3:
                    row[4] = "Near Expiry"
                else:
                    row[4] = "Fresh"

                rows.append(row)

    with open("groceries.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)   # ✅ Write header back
        writer.writerows(rows)

    print("\nExpiry Status Updated Successfully!")
    for row in rows:
        print(row)
    print()

# DELETE FUNCTION

def delete_item():
    item_to_delete = input("Enter item name to delete: ")
    rows = []
    found = False

    with open("groceries.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                if row[0] == item_to_delete and row[4] != "Deleted":
                    row[4] = "Deleted"   # mark instead of removing
                    found = True
                rows.append(row)

    with open("groceries.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    if found:
        print(f"Item '{item_to_delete}' marked as Deleted!\n")
    else:
        print(f"Item '{item_to_delete}' not found or already deleted.\n")

# WASTE FUNCTION 
def waste_report():
    today = datetime.today()
    print("\nWaste Report (Expired Items):")

    with open("groceries.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row

        for row in reader:
            if row:  # avoid empty rows
                expiry_date = datetime.strptime(row[2], "%Y-%m-%d")
                if expiry_date < today:  # already expired
                    print(f"{row[0]} expired on {row[2]}")
    print()

def visualize_data():
    # Read grocery file (assuming CSV)
    df = pd.read_csv("grocery.csv")

    # Group by item and sum quantity
    stock_data = df.groupby("Item")["Quantity"].sum()

    # Plot bar chart
    plt.figure(figsize=(8,5))
    stock_data.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.title("Grocery Stock Analysis", fontsize=14)
    plt.xlabel("Items", fontsize=12)
    plt.ylabel("Quantity", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def stock_analysis():
    # Read CSV normally
    df = pd.read_csv("groceries.csv")

    # Clean column names (remove spaces if any)
    df.columns = df.columns.str.strip()

    # Convert Quantity to numeric (if '5kg' → 5)
    df["Quantity"] = df["Quantity"].astype(str).str.extract(r'(\d+)').astype(float)

    # Check what columns are present
    print("Columns in CSV:", df.columns)

    # Group by item Name
    if "Name" in df.columns:
        stock = df.groupby("Name")["Quantity"].sum()
    else:
        print("⚠️ No 'Name' column found in CSV")
        return

    # Plot bar chart
    stock.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Stock Analysis - Quantity per Item")
    plt.xlabel("Item Name")
    plt.ylabel("Total Quantity")
    plt.show()


def expired_per_month():
    df = pd.read_csv("groceries.csv", names=["Name", "PurchaseDate", "ExpiryDate", "Quantity", "Status"])

    # Convert expiry date
    df["ExpiryDate"] = pd.to_datetime(df["ExpiryDate"], errors="coerce")

    # Filter expired
    expired = df[df["ExpiryDate"] < pd.Timestamp.today()]

    if expired.empty:
        print("✅ No expired items found.")
        return

    # Group by month
    expired["Month"] = expired["ExpiryDate"].dt.to_period("M")
    monthly_counts = expired.groupby("Month").size()

    # Bar chart
    monthly_counts.plot(kind="bar", color="orange", edgecolor="black")
    plt.title("Expired Items per Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Expired Items")
    plt.show()

while True:
    print("\n--- Grocery Management Menu ---")
    print("1. Add Item")
    print("2. View All Items")
    print("3. Check Expiry")
    print("4. Delete Item")
    print("5. Waste Report")
    print("6. Visualize Waste")
    print("7. Stock Analysis")
    print("8. Expired Items per Month (Chart)")
    print("9. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        add_item()
    elif choice == "2":
        list_items()
    elif choice == "3":
        check_expiry()
    elif choice == "4":
        delete_item()
    elif choice == "5":
        waste_report()
    elif choice == "6":
        visualize_data()
    elif choice == "7":
        stock_analysis()
    elif choice == "8":
        expired_per_month()
    elif choice == "9":
        print("Goodbye!")
        break   # ✅ now works because it’s inside while True
    else:
        print("Invalid option. Try again.\n")
