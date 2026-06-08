import json

with open('data/all_india_destinations.json') as f:
    data = json.load(f)

print(f'✅ Total Destinations: {len(data)}')

# Get unique regions and categories
regions = set()
categories = set()
for dest, info in data.items():
    regions.add(info.get('region', 'Unknown'))
    for cat in info.get('category', []):
        categories.add(cat)

print(f'📍 Regions: {len(regions)}')
print(f'🏷️ Categories: {len(categories)}')

# Show region breakdown
region_count = {}
for dest, info in data.items():
    region = info.get('region', 'Unknown')
    region_count[region] = region_count.get(region, 0) + 1

print(f'\n📊 Destinations by Region:')
for region in sorted(region_count.keys()):
    print(f'  • {region}: {region_count[region]}')

print(f'\n🏷️ All Categories: {", ".join(sorted(categories))}')
