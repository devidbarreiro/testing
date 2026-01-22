import os
import glob

media_dir = "media"
print(f"Listing files in {media_dir}:")
files = glob.glob(os.path.join(media_dir, "*"))
found_pie = False

for f in files:
    size = os.path.getsize(f)
    print(f"📄 {os.path.basename(f)} ({size} bytes)")
    if "PIE_CHART" in f or "PieChart" in f:
        found_pie = True

if found_pie:
    print("\n✅✅✅ PIE CHART FOUND! ✅✅✅")
else:
    print("\n❌❌❌ PIE CHART NOT FOUND! ❌❌❌")
