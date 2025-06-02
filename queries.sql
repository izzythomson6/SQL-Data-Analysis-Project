-- Count emails opened
SELECT COUNT(*) AS emails_opened 
FROM email_campaign 
WHERE opened = '1';

--Measuring Open Rates 
--Open rates = opened/total sent
SELECT campaign_name,
COUNT(*) as total_sent,
SUM(CASE WHEN opened = 1 THEN 1
         ELSE 0
         END) AS total_opened,
ROUND(SUM(CASE WHEN opened = 1 THEN 1
               ELSE 0
               END) * 100 / COUNT(*), 2) AS open_rate_percent
FROM email_campaign
GROUP BY campaign_name

--Measuring click through rates
--click through rates = clicked / opened
SELECT 
campaign_name,
COUNT(*) as total_sent,
SUM(CASE WHEN clicked = 1 THEN 1
         ELSE 0
         END) AS total_clicked,
ROUND(SUM(CASE WHEN clicked = 1 THEN 1
               ELSE 0
               END) * 100 / COUNT(*), 2) AS click_rate_percent
FROM email_campaign
GROUP BY campaign_name

--Measuring unsubscribe rates
-- Unsubscribe rate = unsubscribed/total sent
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

--Measuring engagement trends over time 
--Measuring monthly open rates
--would be similar for click rates and unsubscribe rates
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

--Measuring user level engagement metrics
--Being able to identify the most and least engaged users
--Then being able to use this data to target perhaps the least
--in other campaigns
SELECT
user_id,
COUNT(*) AS total_emails_received,
SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS total_opened,
SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) AS total_clicked
FROM email_campaign
GROUP BY user_id
ORDER BY total_opened DESC;

--Engagement data by day of the week
--This is useful in seeing which days have the highest engagement
--and therefore you can plan your campaigns launch based around this
SELECT
campaign_name,
STRFTIME('%w', DATE(substr(send_date, 7, 4) || '-' || substr(send_date, 4, 2) || '-' || substr(send_date, 1, 2))) AS day_of_week,
COUNT(*) AS total_sent,
SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS total_opened,
ROUND(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS open_rate_percent
FROM email_campaign
GROUP BY campaign_name, day_of_week
ORDER BY campaign_name, day_of_week;

--Caculating the average open rate over a month and a running average up to that month
WITH monthly_stats AS (
SELECT
campaign_name,
STRFTIME('%Y-%m', DATE(substr(send_date, 7, 4) || '-' || substr(send_date, 4, 2) || '-' || substr(send_date, 1, 2))) AS year_month,
COUNT(*) AS total_sent,
SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS total_opened,
ROUND(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS open_rate_percent
FROM email_campaign
GROUP BY campaign_name, year_month
)
SELECT
  campaign_name,
  year_month,
  total_sent,
  total_opened,
  open_rate_percent,
  ROUND(AVG(open_rate_percent) OVER (PARTITION BY campaign_name ORDER BY year_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg_open_rate
FROM monthly_stats
ORDER BY campaign_name, year_month;

--Peak day for engagement 
SELECT 
send_date,
SUM(opened) AS total_opens,
SUM(clicked) AS total_clicks
FROM email_campaign
GROUP BY send_date
ORDER BY total_opens DESC, total_clicks DESC
LIMIT 1;