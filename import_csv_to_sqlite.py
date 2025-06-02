import pandas as pd
import sqlite3

# Step 1: Load CSV with pandas
df = pd.read_csv('email_campaign_data.csv')

# Step 2: Connect/create SQLite database file
conn = sqlite3.connect('email_campaign_data.db')

# Step 3: Write the dataframe to SQL table (replace if exists)
df.to_sql('email_campaign', conn, if_exists='replace', index=False)

print("CSV imported to SQLite database successfully!")

# Close the connection
conn.close()