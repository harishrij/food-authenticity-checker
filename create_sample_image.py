# create_sample_image.py
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (1000, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = "Ingredients: Wheat Flour, Sugar, Gelatin, Milk Powder"
d.text((10, 50), text, fill=(0, 0, 0))
img.save('data/sample_labels/label1.jpg')
print("Saved data/sample_labels/label1.jpg")
