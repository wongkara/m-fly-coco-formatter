
import json
from datetime import datetime

# Function to calculate bounding box and area
def calculate_bbox_and_area(min_x, max_x, min_y, max_y):
    width = max_x - min_x
    height = max_y - min_y
    area = width * height
    return [min_x, min_y, width, height], area

# Read input data from input.txt
input_file = "input.txt"
with open(input_file, "r") as f:
    input_data = json.load(f)

# Initialize COCO format dictionary
coco_data = {
    "info": {
        "description": "Rendered blender images w/ objects for M-Fly Object Detection",
        "year": datetime.now().year,
        "contributor": "Kara Wong, Somya Valecha, Marcus Chung",
        "date_created": datetime.now().strftime("%Y/%m/%d")
    },
    "licenses": [
    ],
    "images": [],
    "annotations": [],
    "categories": []
}

# Mapping for categories (extend as needed)
category_mapping = {}
category_id_counter = 0

# Annotation and image ID counters
annotation_id = 1
image_id = 1

# Process input data
for render_key, objects in input_data.items():
    # Add image entry
    coco_data["images"].append({
        "id": image_id,
        "width": 640,
        "height": 640, 
        "file_name": f"{render_key}.jpg",
        "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    for obj_key, bbox_info in objects.items():
        # Extract object category and instance ID
        obj_parts = obj_key.split("_")
        category_name = obj_parts[0]
        
        # Assign category ID if not already mapped
        if category_name not in category_mapping:
            category_mapping[category_name] = category_id_counter
            coco_data["categories"].append({
                "supercategory": category_name,  # Using category name as supercategory
                "id": category_id_counter,
                "name": category_name
            })
            category_id_counter += 1

        category_id = category_mapping[category_name]
        
        # Calculate bbox and area
        bbox, area = calculate_bbox_and_area(
            bbox_info["min_x"], bbox_info["max_x"], bbox_info["min_y"], bbox_info["max_y"]
        )

        # Add annotation entry
        coco_data["annotations"].append({
            "id": annotation_id,
            "category_id": category_id,
            "iscrowd": 0,
            "segmentation": [],  # Add segmentation data if available
            "image_id": image_id,
            "area": area,
            "bbox": bbox
        })
        annotation_id += 1

    image_id += 1

# Save to file or print
output_file = "coco_formatted_data.json"
with open(output_file, "w") as f:
    json.dump(coco_data, f, indent=4)

print(f"COCO formatted data saved to {output_file}")
