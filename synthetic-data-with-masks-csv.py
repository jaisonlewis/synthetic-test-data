import random
import numpy as np
from PIL import Image, ImageDraw
import os
import csv
import cv2

num_images = 10
image_size = 256

os.makedirs('images', exist_ok=True)
os.makedirs('masks', exist_ok=True)

# Create a list to store object information (coordinates and labels)
object_info = []

for i in range(num_images):

    # Create blank black image
    image = np.zeros((image_size, image_size, 3), dtype=np.uint8)

    # Randomly divide into quadrants
    quad_cols = random.choice([2, 3, 4])
    quad_rows = random.choice([2, 3, 4])
    quad_width = image_size // quad_cols
    quad_height = image_size // quad_rows

    for x in range(quad_cols):
        for y in range(quad_rows):

            # Generate object in quadrant
            shape = random.choice(['circle', 'square', 'triangle'])
            obj_size = random.randint(5, min(quad_width, quad_height) // 2)

            # Position object completely inside quadrant
            obj_x = random.randint(x * quad_width + obj_size, (x + 1) * quad_width - obj_size)
            obj_y = random.randint(y * quad_height + obj_size, (y + 1) * quad_height - obj_size)

            # Append object information to the list
            object_info.append([i, shape, obj_x, obj_y, obj_size])

            if shape == 'circle':
                image = cv2.circle(image, (obj_x, obj_y), obj_size, (255, 255, 255), -1)

            elif shape == 'square':
                image = cv2.rectangle(image, (obj_x, obj_y), (obj_x + obj_size, obj_y + obj_size), (255, 0, 0), -1)

            else:
                x2 = obj_x + obj_size
                y2 = obj_y
                x3 = obj_x
                y3 = obj_y + obj_size
                image = cv2.fillConvexPoly(image, np.array([[obj_x, obj_y], [x2, y2], [x3, y3]]), (0, 0, 255))

    # Save color image
    img = Image.fromarray(image)
    img.save(f'images/image_{i}.png')

    # Create a blank white mask image with black outlines
    mask_image = Image.new('L', (image_size, image_size), color=255)
    draw = ImageDraw.Draw(mask_image)

    # Draw object outlines on the mask
    for obj_data in object_info:
        if obj_data[0] == i:
            shape, obj_x, obj_y, obj_size = obj_data[1:]
            if shape == 'circle':
                draw.ellipse([(obj_x - obj_size, obj_y - obj_size), (obj_x + obj_size, obj_y + obj_size)], outline=0)
            elif shape == 'square':
                draw.rectangle([(obj_x, obj_y), (obj_x + obj_size, obj_y + obj_size)], outline=0)
            else:
                x2 = obj_x + obj_size
                y2 = obj_y
                x3 = obj_x
                y3 = obj_y + obj_size
                draw.polygon([(obj_x, obj_y), (x2, y2), (x3, y3)], outline=0)

    # Save mask image
    mask_image.save(f'masks/mask_{i}.png')

print('Generated {} images and masks'.format(num_images))

# Save object information to a .csv file
csv_filename = 'object_coord.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Image_ID', 'Shape', 'X', 'Y', 'Size'])
    csv_writer.writerows(object_info)

print('Object information saved to "{}"'.format(csv_filename))
