import openai
import tiktoken
from constants import Config

openai.api_key = Config.OPENIA_API_KEY


def tokenCount(text):
    enc = tiktoken.get_encoding("p50k_base")
    return len(enc.encode(text))

def chat_gpt(prompt):
    prompt = 'Hello I want to create a 3D virtualization of a bedroom with the following description:\n"'+prompt+'"\n\nI want you to give me a single line description of each object in the room while also picking what category they fall under.\n\nCategories - ["armchair", "Lounge Chair / Cafe Chair / Office Chair", "Pendant Lamp", "Coffee Table", "Corner/Side Table", "Dining Table", "King-size Bed", "Nightstand", "Bookcase / jewelry Armoire", "Three-Seat / Multi-seat Sofa", "TV Stand", "Drawer Chest / Corner cabinet", "Shelf", "Wardrobe", "Footstool / Sofastool / Bed End Stool / Stool", "Sideboard / Side Cabinet / Console Table", "Ceiling Lamp", "Children Cabinet", "Bed Frame", "Round End Table", "Desk", "Single bed", "Loveseat Sofa", "Dining Chair", "Barstool", "Lazy Sofa", "L-shaped Sofa", "Wine Cabinet", "Dressing Table", "Dressing Chair", "Kids Bed", "Classic Chinese Chair", "Bunk Bed", "Chaise Longue Sofa", "Lounge Chair / Book-chair / Computer Chair", "Sideboard / Side Cabinet / Console", "None", "Bar", "Three-Seat / Multi-person sofa", "Double Bed", "Shoe Cabinet", "Couch Bed", "Wine Cooler", "Tea Table", "Hanging Chair", "Folding chair", "U-shaped Sofa", "Two-seat Sofa", "Floor Lamp", "Wall Lamp"]\n\nThe description of the furniture objects I want is ["Bed", "study table", "study chair", "cupboards", "tv stand", "roof light"]\n-------------------------------------------------------------------\nA sample response I am expecting for the bedroom description of: "A fun, boy'+"'"+'s bedroom"\n\nBed: "A race car-inspired bed in a boy'+"'"+'s bedroom, with vibrant colors, sleek design, and fun decals." - Category: "Kids Bed"\n\nStudy Table: "A sleek, blue, wooden study desk in a boy'+"'"+'s bedroom." - Category: "Desk"\n....\n--------------------------------------------------------------------\nRespond in the exact same format as the sample, do not include any extra text.'
    tk = tokenCount(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4097 - tk,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def gpt_out(prompt_input):
    response = chat_gpt(prompt_input)
    furnitures = response.split('\n')
    fin_out = []
    for furniture in (furniture for furniture in furnitures if not furniture == ""):
        furni = furniture.split('"')
        print(furni[1])
        print(furni[3])
        fin_out.append({'Category': furni[3], 'Description': furni[1]})
    return {'Bed': fin_out[0], 'Table': fin_out[1], 'Chair': fin_out[2], 'Wardrobe': fin_out[3], 'TV Stand': fin_out[4], 'Light': fin_out[5]}