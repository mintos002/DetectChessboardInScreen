import os
from PIL import Image

# Path to the directory containing the images
path_to_images = "data/dataset/pieces"

# Path to the file containing the list of background colors
path_to_colors = "data/dataset/pieces/colors.txt"

# Open the file containing the list of background colors
with open(path_to_colors, "r") as f:
    colors = f.readlines()

# Get the first PNG image in the directory
for filename in os.listdir(path_to_images):
    if filename.endswith(".png"):
        image_path = os.path.join(path_to_images, filename)
        break

# Load the image and convert it to RGBA mode
image = Image.open(image_path)
image = image.convert("RGBA")

# Loop over the list of background colors and save a new image for each color
for color in colors:
    # Strip any whitespace and convert the color to an RGB tuple
    color = color.strip()
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    background_color = (r, g, b, 255)

    # Create a new image with the same size as the original image and fill it with the background color
    new_image = Image.new("RGBA", image.size, background_color)

    # Composite the original image onto the new image, using the alpha channel of the original image
    new_image = Image.alpha_composite(new_image, image)

    # Save the new image with the hex color code as the filename
    new_filename = f"{color}.png"
    new_image.save(os.path.join(path_to_images, new_filename))
