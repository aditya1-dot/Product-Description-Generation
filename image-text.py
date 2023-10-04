# Import necessary libraries
import requests
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the Blip processor and model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Load the raw image
raw_image = Image.open("dataset-0/home appliances/microwave/download (1).jpeg")

# Prepare the input for conditional image captioning
text = ' for sale'  # The text to condition the image caption
inputs = processor(raw_image, text, return_tensors="pt", max_length=128, truncation=True)

# Generate image caption with a maximum of 200 new tokens and output scores
out = model.generate(**inputs, max_new_tokens=200, output_scores=True)

# Decode and print the generated image caption
final_caption = processor.decode(out[0], skip_special_tokens=True)
print(final_caption)
