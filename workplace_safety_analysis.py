import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (Replace 'your_file.csv' with your actual file path)
df = pd.read_csv("ITA 300A Summary Data 2023 through 12-31-2024.csv")

# Select relevant columns
df_clean = df[[
    "year_filing_for", "sector", "industry_description", 
    "total_injuries", "total_deaths", "total_dafw_cases", "total_djtr_cases"
]]

# Convert numeric columns to proper data types
numeric_cols = ["total_injuries", "total_deaths", "total_dafw_cases", "total_djtr_cases"]
df_clean[numeric_cols] = df_clean[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Remove rows with missing essential values
df_clean = df_clean.dropna(subset=["year_filing_for", "sector", "industry_description"])

# Filter data for 2023 only
df_2023 = df_clean[df_clean["year_filing_for"] == 2023]

# Sector-Level Analysis
sector_summary = df_2023.groupby("sector")[numeric_cols].sum().reset_index()

# Industry-Level Analysis
industry_summary = df_2023.groupby("industry_description")[numeric_cols].sum().reset_index()

# Plot Injury Trends by Sector
plt.figure(figsize=(12, 6))
plt.barh(sector_summary["sector"], sector_summary["total_injuries"], color="blue")
plt.xlabel("Total Injuries")
plt.ylabel("Sector")
plt.title("Workplace Injuries by Sector (2023)")
plt.gca().invert_yaxis()
plt.show()

# Plot Fatalities by Industry (Top 10 industries with highest fatalities)
top_fatalities_industries = industry_summary.nlargest(10, "total_deaths")

plt.figure(figsize=(12, 6))
plt.barh(top_fatalities_industries["industry_description"], top_fatalities_industries["total_deaths"], color="red")
plt.xlabel("Total Fatalities")
plt.ylabel("Industry")
plt.title("Top 10 Industries with Highest Fatalities (2023)")
plt.gca().invert_yaxis()
plt.show()

# Plot Correlation Between Job Restrictions (DJTR cases) and Injuries
plt.figure(figsize=(8, 6))
plt.scatter(df_2023["total_djtr_cases"], df_2023["total_injuries"], alpha=0.5, color="purple")
plt.xlabel("Total Job Restriction Cases (DJTR)")
plt.ylabel("Total Injuries")
plt.title("Correlation Between Job Restrictions and Injuries (2023)")
plt.show()
