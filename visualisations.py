#Visualisation of the open rates of the campaign
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
conn = sqlite3.connect('email_campaign_data.db')
query = """
SELECT campaign_name,
       COUNT(*) as total_sent,
       SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS total_opened,
       ROUND(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS open_rate_percent
FROM email_campaign
GROUP BY campaign_name
"""
df = pd.read_sql_query(query, conn)
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(x='campaign_name', y='open_rate_percent', data=df, palette='Blues_d')
plt.title('Open Rate by Campaign')
plt.xlabel('Campaign Name')
plt.ylabel('Open Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

click_rate_query = '''
SELECT 
    campaign_name,
    COUNT(*) as total_sent,
    SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) AS total_clicked,
    ROUND(SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS click_rate_percent
FROM email_campaign
GROUP BY campaign_name;
'''
click_df = pd.read_sql_query(click_rate_query, conn)
plt.figure(figsize=(8, 5))
plt.bar(click_df['campaign_name'], click_df['click_rate_percent'], color='lightgreen')
plt.title('Click-Through Rate by Campaign')
plt.xlabel('Campaign')
plt.ylabel('Click Rate (%)')
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

unsubscribe_rate_query = '''
SELECT 
campaign_name,
COUNT(*) as total_sent,
SUM(CASE WHEN unsubscribed = 1 THEN 1
         ELSE 0
         END) AS total_unsubscribed,
ROUND(SUM(CASE WHEN unsubscribed = 1 THEN 1
               ELSE 0
               END) * 100 / COUNT(*), 2) as unsubscribe_rate_percent
FROM email_campaign
GROUP BY campaign_name
'''
unsubscribe_df = pd.read_sql_query(unsubscribe_rate_query, conn)
plt.figure(figsize=(8, 5))
plt.bar(unsubscribe_df['campaign_name'], unsubscribe_df['unsubscribe_rate_percent'], color='lightgreen')
plt.title('Unsubscribe Rate by Campaign')
plt.xlabel('Campaign')
plt.ylabel('Unsubscribe Rate (%)')
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

#Measuring engagement rates over time
engagement_rate_query = '''
SELECT
campaign_name,
STRFTIME('%Y-%m', DATE(substr(send_date, 7, 4) || '-' || substr(send_date, 4, 2) || '-' || substr(send_date, 1, 2))) AS year_month,
COUNT(*) AS total_sent,
SUM(CASE WHEN opened = 1 THEN 1
         ELSE 0 END) AS total_opened,
ROUND(SUM(CASE WHEN opened = 1 THEN 1 
               ELSE 0 END) * 100.0/ COUNT(*),2) as open_rate_percent
FROM email_campaign
GROUP BY campaign_name, year_month
ORDER BY campaign_name, year_month
'''
engagementdf = pd.read_sql_query(engagement_rate_query, conn)
engagementdf['year_month'] = pd.to_datetime(engagementdf['year_month'])
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=engagementdf, x='year_month', y='open_rate_percent', hue='campaign_name', marker='o')

plt.title('Monthly Email Open Rates by Campaign')
plt.xlabel('Month')
plt.ylabel('Open Rate (%)')
plt.xticks(rotation=45)
plt.legend(title='Campaign')
plt.tight_layout()
plt.show()


#engagement data by week 
engagement_week_data_query = '''
SELECT
campaign_name,
STRFTIME('%w', DATE(substr(send_date, 7, 4) || '-' || substr(send_date, 4, 2) || '-' || substr(send_date, 1, 2))) AS day_of_week,
COUNT(*) AS total_sent,
SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS total_opened,
ROUND(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS open_rate_percent
FROM email_campaign
GROUP BY campaign_name, day_of_week
ORDER BY campaign_name, day_of_week;
'''
engagement_week_df = pd.read_sql_query(engagement_week_data_query, conn)
engagement_week_df['day_of_week'] = engagement_week_df['day_of_week'].astype(int)
engagement_week_df['day_name'] = engagement_week_df['day_of_week'].apply(lambda x: calendar.day_name[x])
day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=engagement_week_df, 
             x='day_name', 
             y='open_rate_percent', 
             hue='campaign_name', 
             marker='o',
             hue_order=engagement_week_df['campaign_name'].unique(),
             sort=False)

plt.title('Email Open Rates by Day of Week and Campaign')
plt.xlabel('Day of Week')
plt.ylabel('Open Rate (%)')
plt.xticks(ticks=range(len(day_order)), labels=day_order)
plt.legend(title='Campaign')
plt.tight_layout()
plt.show()

conn.close()
