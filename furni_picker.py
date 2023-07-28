import json
from constants import Config
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os
import random


def picker(data):
    model_info = json.load(open(Config.FUTURE_PATH + '/model_info.json', 'r', encoding='utf-8'))
    category = {}

    for model in model_info:
        if model['category'] and not model['category'] in category:
            category[model['category'].lower()] = []

    for model in model_info:
        if model['category']:
            category[model['category'].lower()].append(model['model_id'])

    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    image_dir = Config.FUTURE_IMAGE_PATH

    furnitures = []
    for type in data:
        cat = data[type]['Category'] if type != "Table" else "Desk"
        desc = data[type]['Description']
        most_similar_image = None
        max_similarity_score = -1
        for i, id in enumerate(id for id in category[cat.lower()] if id):
            image_path = os.path.join(image_dir, id + ".jpg")
            image = Image.open(image_path)
            inputs = processor(text=desc, images=image, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            logits_per_image = outputs.logits_per_image
            similarity_score =  logits_per_image.item()
            print(f"{i + 1}: {similarity_score}")
            if similarity_score > max_similarity_score:
                max_similarity_score = similarity_score
                most_similar_image = id + ".jpg"
        print(f"Type: {type}, Most similar image path: {os.path.join(image_dir, most_similar_image)}, Similarity score: {max_similarity_score}")
        image_path = os.path.join(image_dir, most_similar_image)
        image = Image.open(image_path)
        image.show()
        furnitures.append(most_similar_image.replace(".jpg",""))
    return {'Bed': furnitures[0], 'Table': furnitures[1], 'Chair': furnitures[2], 'Wardrobe': furnitures[3], 'TV Stand': furnitures[4], 'Light': furnitures[5]}


def rand_picker():
    model_info = json.load(open(Config.FUTURE_PATH + '/model_info.json', 'r', encoding='utf-8'))
    category = {}

    for model in model_info:
        if model['category'] and not model['category'] in category:
            category[model['category']] = []

    for model in model_info:
        if model['category']:
            category[model['category']].append(model['model_id'].lower())

    return {'Bed': random.choices(category['King-size Bed'])[0], 'Table': random.choices(category['Desk'])[0], 'Chair': random.choices(category['Lounge Chair / Book-chair / Computer Chair'])[0], 'Wardrobe': random.choices(category['Wardrobe'])[0], 'TV Stand': random.choices(category['TV Stand'])[0], 'Light': random.choices(category['Pendant Lamp'])[0]}
