from PIL import Image
import os

src = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'b3d48b270d6a03b1723d1ed58219d00.jpg')
img = Image.open(src)
w, h = img.size

# Divide image into a 4x6 grid and analyze each cell
rows, cols = 6, 4
cell_h = h // rows
cell_w = w // cols

print("Grid analysis (4x6) - each cell's dominant characteristics:")
print("(D=dark, L=light, M=medium | R=red, G=green, B=blue, N=neutral | S=saturated)")
print("-" * 70)

grid = []
for row in range(rows):
    row_data = []
    for col in range(cols):
        x1, y1 = col * cell_w, row * cell_h
        x2, y2 = (col + 1) * cell_w, (row + 1) * cell_h
        region = img.crop((x1, y1, x2, y2)).resize((30, 30))
        pixels = list(region.getdata())
        avg_r = sum(p[0] for p in pixels) // len(pixels)
        avg_g = sum(p[1] for p in pixels) // len(pixels)
        avg_b = sum(p[2] for p in pixels) // len(pixels)
        brightness = 0.299 * avg_r + 0.587 * avg_g + 0.114 * avg_b
        mx = max(avg_r, avg_g, avg_b)
        mn = min(avg_r, avg_g, avg_b)
        sat = mx - mn
        
        # Check variance (texture)
        variance = sum((0.299*p[0]+0.587*p[1]+0.114*p[2] - brightness)**2 for p in pixels) / len(pixels)
        
        bri_char = 'D' if brightness < 80 else ('L' if brightness > 180 else 'M')
        color_char = 'R' if avg_r > avg_g + 10 and avg_r > avg_b + 10 else ('G' if avg_g > avg_r + 10 and avg_g > avg_b + 10 else ('B' if avg_b > avg_r + 10 and avg_b > avg_g + 10 else 'N'))
        sat_char = '*' if sat > 50 else ''
        var_char = '~' if variance > 1000 else ''
        
        row_data.append(f"[{bri_char}{color_char}{sat_char}{var_char}]")
    grid.append(" ".join(row_data))

for i, row in enumerate(grid):
    print(f"Row {i}: {row}")

# Now check for specific patterns - look at vertical strips
print("\n\nVertical strip analysis (left to right):")
for i in range(8):
    x1 = i * w // 8
    x2 = (i + 1) * w // 8
    strip = img.crop((x1, 0, x2, h)).resize((20, 60))
    pixels = list(strip.getdata())
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)
    brightness = 0.299 * avg_r + 0.587 * avg_g + 0.114 * avg_b
    variance = sum((0.299*p[0]+0.587*p[1]+0.114*p[2] - brightness)**2 for p in pixels) / len(pixels)
    print(f"  Strip {i} ({x1}-{x2}px): brightness={brightness:.0f}, variance={variance:.0f}, RGB=({avg_r},{avg_g},{avg_b})")

# Check horizontal strips
print("\nHorizontal strip analysis (top to bottom):")
for i in range(8):
    y1 = i * h // 8
    y2 = (i + 1) * h // 8
    strip = img.crop((0, y1, w, y2)).resize((60, 20))
    pixels = list(strip.getdata())
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)
    brightness = 0.299 * avg_r + 0.587 * avg_g + 0.114 * avg_b
    variance = sum((0.299*p[0]+0.587*p[1]+0.114*p[2] - brightness)**2 for p in pixels) / len(pixels)
    print(f"  Strip {i} ({y1}-{y2}px): brightness={brightness:.0f}, variance={variance:.0f}, RGB=({avg_r},{avg_g},{avg_b})")

# Find unique colors (quantized)
print("\n\nTop 10 dominant colors (quantized to 32 levels):")
from collections import Counter
small = img.resize((100, 150))
pixels = list(small.getdata())
quantized = [(p[0]//32*32, p[1]//32*32, p[2]//32*32) for p in pixels]
color_counts = Counter(quantized).most_common(10)
total = len(pixels)
for color, count in color_counts:
    pct = count / total * 100
    print(f"  RGB{color}: {pct:.1f}%")
