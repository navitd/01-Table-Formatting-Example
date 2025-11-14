"""
Script to create an animated GIF showing data transformation
Input table -> Arrow -> Output table
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Animation settings
FRAME_WIDTH = 1200
FRAME_HEIGHT = 400
PADDING = 40
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
HEADER_COLOR = (0, 32, 96)  # Dark blue
HEADER_TEXT_COLOR = (255, 255, 255)
ARROW_COLOR = (0, 100, 200)
BORDER_COLOR = (200, 200, 200)

# Create font (will use default if custom font not available)
try:
    title_font = ImageFont.truetype("arial.ttf", 16)
    text_font = ImageFont.truetype("arial.ttf", 12)
except:
    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()

def draw_table(image, title, data, x_offset, y_offset, col_widths):
    """Draw a table on the image"""
    draw = ImageDraw.Draw(image)
    
    # Draw title
    draw.text((x_offset, y_offset - 30), title, fill=TEXT_COLOR, font=title_font)
    
    # Table position
    table_x = x_offset
    table_y = y_offset
    cell_height = 30
    
    # Draw header row
    current_x = table_x
    for i, (header, width) in enumerate(zip(data[0], col_widths)):
        # Draw header cell background
        draw.rectangle(
            [current_x, table_y, current_x + width, table_y + cell_height],
            fill=HEADER_COLOR,
            outline=BORDER_COLOR
        )
        # Draw header text
        draw.text(
            (current_x + 5, table_y + 7),
            header,
            fill=HEADER_TEXT_COLOR,
            font=text_font
        )
        current_x += width
    
    # Draw data rows (only first 3)
    for row_idx, row in enumerate(data[1:4]):
        table_y += cell_height
        current_x = table_x
        for col_idx, (cell, width) in enumerate(zip(row, col_widths)):
            # Draw cell border
            draw.rectangle(
                [current_x, table_y, current_x + width, table_y + cell_height],
                fill=BG_COLOR,
                outline=BORDER_COLOR
            )
            # Draw text (truncate if too long)
            text = str(cell)[:width // 10]
            draw.text(
                (current_x + 5, table_y + 7),
                text,
                fill=TEXT_COLOR,
                font=text_font
            )
            current_x += width

def draw_arrow(image, x, y):
    """Draw a large arrow pointing right"""
    draw = ImageDraw.Draw(image)
    arrow_length = 60
    
    # Arrow shaft
    draw.rectangle(
        [x, y - 5, x + arrow_length, y + 5],
        fill=ARROW_COLOR
    )
    
    # Arrow head (triangle)
    draw.polygon(
        [(x + arrow_length, y - 15), (x + arrow_length, y + 15), (x + arrow_length + 15, y)],
        fill=ARROW_COLOR
    )

def create_animation():
    """Create animated GIF"""
    frames = []
    
    # Input table data
    input_headers = ["record_id", "technology", "bandwidth"]
    input_data = [
        input_headers,
        ["E5015", "LTE", "10"],
        ["E5015", "LTE", "10"],
        ["E5015", "5G", "100"],
    ]
    
    # Output table data
    output_headers = ["Tower ID", "Type", "4G_BW", "5G_BW"]
    output_data = [
        output_headers,
        ["E5015", "Macro", "20", "100"],
        ["E0092", "Micro", "15", "0"],
        ["E0093", "Macro", "30", "50"],
    ]
    
    col_widths_input = [120, 120, 120]
    col_widths_output = [100, 100, 100, 100]
    
    # Frame 1: Show input table (hold for 2 seconds = 20 frames at 100ms)
    for _ in range(20):
        img = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), BG_COLOR)
        draw_table(img, "INPUT: Raw CSV Data (Multiple rows per tower)", input_data, 50, 100, col_widths_input)
        frames.append(img)
    
    # Frame 2: Show input + animated arrow (10 frames for arrow animation)
    for i in range(10):
        img = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), BG_COLOR)
        draw_table(img, "INPUT: Raw CSV Data (Multiple rows per tower)", input_data, 50, 100, col_widths_input)
        
        # Animated arrow moving right
        arrow_x = 350 + (i * 4)
        draw_arrow(img, arrow_x, 170)
        
        frames.append(img)
    
    # Frame 3: Show output table (hold for 2 seconds)
    for _ in range(20):
        img = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), BG_COLOR)
        draw_table(img, "OUTPUT: Aggregated & Formatted Data", output_data, 50, 100, col_widths_output)
        frames.append(img)
    
    # Frame 4: Both tables with arrow (final frame, hold for 3 seconds)
    for _ in range(30):
        img = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), BG_COLOR)
        draw_table(img, "INPUT", input_data, 30, 100, [80, 80, 80])
        draw_arrow(img, 300, 170)
        draw_table(img, "OUTPUT", output_data, 420, 100, [80, 70, 70, 70])
        frames.append(img)
    
    # Save as GIF
    output_file = "transformation_animation.gif"
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # 100ms per frame
        loop=0  # Loop forever
    )
    
    print(f"✅ Animation created: {output_file}")
    print(f"   Total frames: {len(frames)}")
    print(f"   Duration: {len(frames) * 0.1:.1f} seconds")

if __name__ == "__main__":
    create_animation()
