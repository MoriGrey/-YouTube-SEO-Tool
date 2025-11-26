"""
Create placeholder icons for the extension.
This script creates simple PNG icons using PIL/Pillow.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create icon directory if it doesn't exist
    icon_dir = os.path.join(os.path.dirname(__file__), "icons")
    os.makedirs(icon_dir, exist_ok=True)
    
    # Icon sizes
    sizes = [16, 48, 128]
    
    for size in sizes:
        # Create a simple icon with text
        img = Image.new('RGB', (size, size), color='#4a9eff')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple "Y" or "SEO" text
        try:
            # Try to use a font (may not work on all systems)
            font_size = size // 2
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        text = "🎸" if size >= 48 else "Y"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        position = ((size - text_width) // 2, (size - text_height) // 2)
        draw.text(position, text, fill='white', font=font)
        
        # Save icon
        icon_path = os.path.join(icon_dir, f"icon{size}.png")
        img.save(icon_path)
        print(f"Created {icon_path}")
    
    print("✅ Icons created successfully!")
    
except ImportError:
    print("PIL/Pillow not installed. Creating simple SVG icons instead...")
    
    # Create simple SVG icons as fallback
    icon_dir = os.path.join(os.path.dirname(__file__), "icons")
    os.makedirs(icon_dir, exist_ok=True)
    
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">
  <rect width="{size}" height="{size}" fill="#4a9eff"/>
  <text x="50%" y="50%" font-family="Arial" font-size="{font_size}" fill="white" text-anchor="middle" dominant-baseline="middle">🎸</text>
</svg>"""
    
    sizes = [16, 48, 128]
    for size in sizes:
        font_size = size // 2
        icon_path = os.path.join(icon_dir, f"icon{size}.png")
        # Note: This creates SVG, but we need PNG. We'll create a simple workaround.
        with open(icon_path.replace('.png', '.svg'), 'w') as f:
            f.write(svg_content.format(size=size, font_size=font_size))
        print(f"Created {icon_path.replace('.png', '.svg')} (SVG fallback)")
    
    print("⚠️ SVG icons created. For PNG icons, install Pillow: pip install Pillow")

