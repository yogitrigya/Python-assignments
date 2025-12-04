#Name :Trigya Yogi
#Date:3 December 2025
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(20)

# Defining parameters for the synthetic dataset (one year of data)
START_DATE = '2025-04-01'
DAYS = 365

print("--- Starting Simplified Weather Data Analysis Lab ---")

dates = pd.to_datetime(START_DATE) + pd.to_timedelta(np.arange(DAYS), unit='D')

temp_base = 10 + 15 * np.sin(np.arange(DAYS) * 2 * np.pi / 365)
temperature = temp_base + np.random.normal(0, 1.5, DAYS)

humidity = np.clip(np.random.normal(65, 5, DAYS), 50, 90)

precipitation = np.abs(np.random.normal(1, 2, DAYS))
precipitation[precipitation < 0.5] = 0.0

df = pd.DataFrame({
    'Date': dates,
    'Temp_C': temperature.round(1),
    'Precip_mm': precipitation.round(1),
    'Humidity_pct': humidity.round(1)
})
df = df.set_index('Date')


nan_indices = np.random.choice(df.index, size=3, replace=False)
df.loc[nan_indices, 'Temp_C'] = np.nan

print(f"\nData generated. Contains {df['Temp_C'].isna().sum()} missing values in Temperature.")


print("Starting simple data cleaning (Mean Imputation)...")

mean_temp = df['Temp_C'].mean()
df['Temp_C_Cleaned'] = df['Temp_C'].fillna(mean_temp).round(1)

print("Cleaning complete.")


print("Starting data analysis: Calculating monthly averages...")

df['Month'] = df.index.month

monthly_avg_temp = df.groupby('Month')['Temp_C_Cleaned'].mean().to_frame()
monthly_avg_temp = monthly_avg_temp.rename(columns={'Temp_C_Cleaned': 'Avg_Monthly_Temp'})

yearly_avg_temp = df['Temp_C_Cleaned'].mean()


print("Generating visualization (Monthly Temperature Bar Chart)...")

plt.figure(figsize=(9, 6))
plt.style.use('seaborn-v0_8-deep')

plt.bar(monthly_avg_temp.index, monthly_avg_temp['Avg_Monthly_Temp'], color='#FF7F0E', alpha=0.8)

plt.title('Average Monthly Temperature for the Year', fontsize=16)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.xlabel('Month', fontsize=12)

plt.axhline(yearly_avg_temp, color='navy', linestyle='--', linewidth=1.5, label=f'Yearly Average: {yearly_avg_temp:.1f}°C')
plt.xticks(monthly_avg_temp.index) # Ensure ticks are on the month numbers
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

print("Visualization complete.")

hottest_month_num = monthly_avg_temp['Avg_Monthly_Temp'].idxmax()
hottest_month_temp = monthly_avg_temp['Avg_Monthly_Temp'].max()

print("\n--- Summary Insights for Sustainability Report ---")
print(f"1. Yearly Average Temperature: {yearly_avg_temp:.1f}°C. This is the baseline temperature for the campus.")
print(f"2. Peak Temperature Month: Month {hottest_month_num} recorded the highest average temperature of {hottest_month_temp:.1f}°C.")
print("3. Sustainability Action: The peak month indicates when cooling energy demand will be highest. The campus should focus on improving insulation or optimizing AC usage during this time.")
