import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_csv('Race_Data.csv')
df2 = pd.read_csv('Qualifying_Data.csv')
df1 = df1.replace('NC', pd.NA).dropna()
df2 = df2.replace('NC', pd.NA).dropna()

df1['Race_ID'] = (df1.index // 20) + 1
df2['Race_ID'] = (df2.index // 20) + 1

merged_df = pd.merge(df1, df2, on=['Race_ID', 'Driver', 'Car'], suffixes=('_Race', '_Qual'))

merged_df['Qual'] = pd.to_numeric(merged_df['Qual'], errors='coerce')
merged_df['Pos'] = pd.to_numeric(merged_df['Pos'], errors='coerce')

merged_df.to_csv('f1_race_data.csv', index=False)

merged_df['Position_Change'] = merged_df['Qual'] - merged_df['Pos']
correlation = merged_df['Qual'].corr(merged_df['Pos'])
print(f'Correlation between qualifying and final positions: {correlation}')

team_colors = {
    'Red Bull Racing Honda RBPT': '#1e41ff',
    'Aston Martin Aramco Mercedes': '#006f62',
    'Ferrari': '#dc0000',
    'Mercedes': '#00d2be',
    'Alfa Romeo Ferrari': '#900000',
    'Alpine Renault': '#0090ff',
    'Williams Mercedes': '#005aff',
    'AlphaTauri Honda RBPT': '#2b4562',
    'Haas Ferrari': '#808080',
    'McLaren Mercedes': '#ff8700'
}

merged_df['Team_Color'] = merged_df['Car'].map(team_colors)

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Qual', y='Pos', data=merged_df, hue='Car', palette=team_colors, legend='full', marker='o')
plt.title('Qualifying vs. Final Positions')
plt.xlabel('Qualifying Position')
plt.ylabel('Final Position')
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.text(5, 20, f'Correlation: {correlation:.2f}', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
plt.tight_layout()
plt.savefig('/Users/varunramanathan/Downloads/qualifying_vs_final_positions.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(merged_df['Position_Change'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Position Changes During Race')
plt.xlabel('Position Change')
plt.ylabel('Frequency')
plt.axvline(x=0, color='red', linestyle='--')
plt.savefig('/Users/varunramanathan/Downloads/distribution_of_position_changes.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='Position_Change', data=merged_df, color='lightgreen')
plt.title('Box Plot of Position Changes')
plt.xlabel('Position Change')
plt.savefig('/Users/varunramanathan/Downloads/box_plot_of_position_changes.png')
plt.show()

plt.figure(figsize=(10, 6))
avg_position_change_by_driver = merged_df.groupby('Driver')['Position_Change'].mean().sort_values()
driver_teams = merged_df.drop_duplicates('Driver').set_index('Driver')['Car']
driver_colors = driver_teams.map(team_colors)
for driver, change in avg_position_change_by_driver.items():
    plt.barh(driver, change, color=driver_colors[driver])
plt.title('Average Position Change by Driver')
plt.xlabel('Average Position Change')
plt.ylabel('Driver')
plt.tight_layout()
plt.savefig('/Users/varunramanathan/Downloads/average_position_change_by_driver_colored.png')
plt.show()
