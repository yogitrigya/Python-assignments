#Name:Trigya Yogi
#Date:4 December 2025
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

def generate_dummy_data(data_dir='data'):
    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)

    start_date = pd.to_datetime('2024-03-01 00:00:00')
    end_date = pd.to_datetime('2024-03-31 23:00:00')
    time_index = pd.date_range(start=start_date, end=end_date, freq='H')

    buildings = ['Research_Lab', 'Library', 'Dormitory']
    
    print(f"Generating {len(buildings)} dummy data files in '{data_dir}/'...")

    for building in buildings:
        base_usage = {'Research_Lab': 150, 'Library': 80, 'Dormitory': 50}[building]
        
        kwh = base_usage + np.random.normal(0, 15, len(time_index))
        peak_factor = np.where((time_index.hour >= 8) & (time_index.hour <= 18), 1.5, 1.0)
        kwh = kwh * peak_factor
        
        kwh[kwh < 0] = 0
        
        df = pd.DataFrame({
            'Timestamp': time_index,
            'kWh': kwh.round(2),
        })
        
        filename = data_path / f"{building}_Mar2024.csv"
        df.to_csv(filename, index=False)
        print(f"  - Created {filename.name}")
    print("-" * 30)

def ingest_and_validate_data(data_dir='data'):
    data_path = Path(data_dir)
    if not data_path.is_dir():
        print(f"Error: Data directory '{data_dir}' not found.")
        return None
        
    all_files = list(data_path.glob("*.csv"))
    df_list = []
    
    print("Task 1: Ingesting and Validating Data")
    
    for file_path in all_files:
        building_name = file_path.stem.split('_')[0] 
        
        try:
            df = pd.read_csv(file_path, on_bad_lines='skip', usecols=[0, 1], names=['Timestamp', 'kWh'], header=0) 
            
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce') 
            df = df.dropna(subset=['Timestamp', 'kWh'])

            df['Building'] = building_name
            df_list.append(df)
            print(f"  - Successfully loaded: {file_path.name} ({len(df)} records)")
            
        except FileNotFoundError:
            print(f"Logging: Missing file at {file_path}. Skipping.")
        except Exception as e:
            print(f"Logging: Error reading {file_path.name}: {e}. Skipping.")

    if df_list:
        df_combined = pd.concat(df_list, ignore_index=True)
        df_combined = df_combined.set_index('Timestamp').sort_index()
        df_combined['kWh'] = pd.to_numeric(df_combined['kWh'], errors='coerce')
        df_combined = df_combined.dropna(subset=['kWh'])
        print(f"Task 1 Complete. Total combined records: {len(df_combined):,}")
        return df_combined
    else:
        print("No valid CSV files found or processed.")
        return None

def calculate_daily_totals(df):
    print("Task 2: Calculating daily campus totals...")
    return df['kWh'].resample('D').sum().rename('Daily_Total_kWh')

def calculate_weekly_aggregates(df):
    print("Task 2: Calculating weekly building aggregates...")
    weekly_data = df.groupby('Building')['kWh'].resample('W').agg(['sum', 'mean']).rename(
        columns={'sum': 'Weekly_Total_kWh', 'mean': 'Weekly_Avg_kWh'})
    return weekly_data

def building_wise_summary(df):
    print("Task 2: Generating building summary table...")
    summary = df.groupby('Building')['kWh'].agg(['mean', 'min', 'max', 'sum']).reset_index()
    return summary

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp 
        self.kwh = kwh

class Building:
    def __init__(self, name, df_readings):
        self.name = name
        self.df_readings = df_readings.copy()
    
    def calculate_total_consumption(self):
        return self.df_readings['kWh'].sum()
        
    def get_max_hourly_usage(self):
        return self.df_readings['kWh'].max()

class BuildingManager:
    def __init__(self):
        self.buildings = {}
        
    def populate_from_df(self, df_combined):
        print("Task 3: Populating OOP Model...")
        for name, group_df in df_combined.groupby('Building'):
            building = Building(name, group_df)
            self.buildings[name] = building
            
    def generate_report(self):
        report = {}
        for name, building in self.buildings.items():
            report[name] = {
                'Total_kWh': building.calculate_total_consumption(),
                'Max_Hourly_kWh': building.get_max_hourly_usage()
            }
        return report

def generate_dashboard(df_combined, df_daily, df_weekly_building):
    print("Task 4: Generating Visualization (dashboard.png)...")
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 12)) 
    plt.style.use('seaborn-v0_8-darkgrid')
    
    ax1 = axes[0, 0]
    daily_building_trend = df_combined.groupby('Building')['kWh'].resample('D').sum()
    daily_building_trend.unstack().plot(ax=ax1, linewidth=2)
    ax1.set_title('Daily Consumption Trend Across All Buildings', fontsize=16)
    ax1.set_ylabel('Energy (kWh)')
    ax1.set_xlabel('Date')
    ax1.legend(title='Building')
    
    ax2 = axes[0, 1]
    avg_weekly_usage = df_weekly_building['Weekly_Total_kWh'].groupby('Building').mean().sort_values(ascending=False)
    avg_weekly_usage.plot(kind='bar', ax=ax2, color=plt.cm.Paired.colors) 
    ax2.set_title('Average Weekly Total Consumption by Building', fontsize=16)
    ax2.set_ylabel('Average Weekly Consumption (kWh)')
    ax2.set_xlabel('Building Name')
    ax2.tick_params(axis='x', rotation=45)
    
    ax3 = axes[1, 0]
    df_combined['Hour'] = df_combined.index.hour 
    peak_analysis = df_combined.groupby(['Building', 'Hour'])['kWh'].mean().reset_index()
    
    for building_name, data in peak_analysis.groupby('Building'):
        scatter_size = data['kWh'] / data['kWh'].max() * 150
        ax3.scatter(data['Hour'], data['kWh'], label=building_name, alpha=0.7, s=scatter_size)
        
    ax3.set_title('Average Hourly Consumption by Building', fontsize=16)
    ax3.set_ylabel('Average Hourly Consumption (kWh)')
    ax3.set_xlabel('Hour of Day (0-23)')
    ax3.set_xticks(range(0, 24, 2))
    ax3.legend(title='Building')
    
    axes[1, 1].axis('off') 

    plt.suptitle('Campus Energy Usage Dashboard', fontsize=24, y=1.02, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    
    plt.savefig('dashboard.png')
    print("Task 4 Complete. Dashboard saved as dashboard.png.")

def generate_executive_summary(df_combined, df_summary_table):
    print("Task 5: Generating Summary Report and Exporting Data...")

    total_campus_consumption = df_combined['kWh'].sum()
    
    highest_consumer = df_summary_table.loc[df_summary_table['sum'].idxmax()]
    
    df_combined['Hour'] = df_combined.index.hour
    peak_load_hour = df_combined.groupby('Hour')['kWh'].mean().idxmax()
    
    core_hour_consumption = df_combined[df_combined.index.hour.isin(range(8, 19))]['kWh'].mean()
    off_hour_consumption = df_combined[~df_combined.index.hour.isin(range(8, 19))]['kWh'].mean()
    
    trend_insight = (f"Core working hours (8AM-7PM) see significantly higher average consumption "
                     f"({core_hour_consumption:.2f} kWh/hr) compared to off-peak hours "
                     f"({off_hour_consumption:.2f} kWh/hr).")
    
    summary_report = f"""
    *** Executive Energy Consumption Summary ***
    
    This report summarizes campus electricity usage data from {df_combined.index.min().strftime('%Y-%m-%d')} to {df_combined.index.max().strftime('%Y-%m-%d')}.
    
    1. Total Campus Consumption: {total_campus_consumption:,.2f} kWh
    
    2. Highest Consuming Building:
       - Building: {highest_consumer['Building']}
       - Total Consumption: {highest_consumer['sum']:,.2f} kWh (accounting for {highest_consumer['sum'] / total_campus_consumption * 100:.1f}% of total load)
    
    3. Peak Load Time:
       - The campus sees its highest average load during the {peak_load_hour}:00 hour.
       
    4. Key Trend Insight:
       - {trend_insight}
       
    ---
    Administrative Recommendation: Implement energy reduction strategies targeting the {highest_consumer['Building']} during the peak load window of {peak_load_hour}:00. The strong difference between core and off-peak hours suggests potential savings through automated shutdown protocols.

    
    df_combined.to_csv('cleaned_energy_data.csv')
    df_summary_table.to_csv('building_summary.csv', index=False)
    
    with open('summary.txt', 'w') as f:
        f.write(summary_report)
        
    print(f"Task 5 Complete. Exported cleaned_energy_data.csv, building_summary.csv, and summary.txt.")
    print("\n" + "="*40)
    print("GENERATED EXECUTIVE SUMMARY")
    print("="*40)
    print(summary_report)
    print("="*40)


def main():
    generate_dummy_data()

    df_combined = ingest_and_validate_data()
    if df_combined is None:
        print("Script terminated due to failed data ingestion.")
        return

    df_daily = calculate_daily_totals(df_combined)
    df_weekly_building = calculate_weekly_aggregates(df_combined)
    df_summary_table = building_wise_summary(df_combined)

    manager = BuildingManager()
    manager.populate_from_df(df_combined)

    generate_dashboard(df_combined.copy(), df_daily, df_weekly_building)

    generate_executive_summary(df_combined, df_summary_table)
    
    print("\n--- Project Pipeline Execution Complete ---")


if __name__ == "__main__":
    if Path('dashboard.png').exists(): os.remove('dashboard.png')
    if Path('cleaned_energy_data.csv').exists(): os.remove('cleaned_energy_data.csv')
    if Path('building_summary.csv').exists(): os.remove('building_summary.csv')
    if Path('summary.txt').exists(): os.remove('summary.txt')
    
    main()
