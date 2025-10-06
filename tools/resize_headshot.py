from PIL import Image
import os

src = r"c:\Users\nickp\OneDrive - Indiana University\Desktop\AI Driven Development\AIDD Assignment 5\images\Professional_Headshot.jpg"
out_dir = os.path.dirname(src)
base_name = 'Professional_Headshot'

sizes = [200, 400, 800]

img = Image.open(src)
# Ensure RGBA or RGB
if img.mode not in ('RGB','RGBA'):
    img = img.convert('RGB')

w,h = img.size
mn = min(w,h)
left = (w-mn)//2
upper = (h-mn)//2
box = (left,upper,left+mn,upper+mn)
square = img.crop(box)

for s in sizes:
    out_path = os.path.join(out_dir, f"{base_name}_{s}.jpg")
    resized = square.resize((s,s), Image.LANCZOS)
    resized.save(out_path, quality=90, optimize=True)
    print('Wrote', out_path)

print('Done')
