import logging
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from gpt4all import GPT4All
import streamlit as st
import json
from streamlit_lottie import st_lottie_spinner

# setting the logging function
logging.getLogger(' ').handlers = []
def setup_logging():
    logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO, force=True,
                        format='%(asctime)s - %(levelname)s: %(message)s')

# function to load json files for animations   
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# function to generate image captions
def generate_image_caption(image_path, text_to_condition,max_new_tokens=50):
    try:
        processor,model,x=model_loader()
        # Load the raw image
        raw_image = Image.open(image_path)
        # Prepare the input for conditional image captioning
        inputs = processor(raw_image, text_to_condition, return_tensors="pt", max_length=128, truncation=True)
        # Generate image caption with a maximum of `max_new_tokens` new tokens and output scores
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, output_scores=True)
        # Decode and return the generated image caption
        final_caption = processor.decode(out[0], skip_special_tokens=True)
        logging.info("Caption generated succesfully.")
        logging.info(final_caption)
        image_displayer(image_path)
  
        return final_caption
    except Exception as e:
        error_message = "Please refresh the website or try after sometime.\nThere is an error due to an interrupted server connection."
        logging.critical("Falcon Model crashed.")  # Log the error message if there's an issue
        st.warning(f':red[{error_message}]')
        return None

# function to generate product description
def generate_product_description(prompt):
    try:
        generating=load_lottiefile("/Users/adityasinha/Desktop/PROJECT/setmax/product_desc.json")
        with st_lottie_spinner(animation_source=generating,height=45,width=45):
            dy_text=st.empty()
            x,y,model=model_loader()
            response=""
            # Generate response for your prompt.
            for token in model.generate(prompt, max_tokens=900,streaming=True,temp=0.5,repeat_penalty=1.4,n_batch=10):
                response+=token
                dy_text.write(response)
            
        logging.info("Description created successfully.")
        logging.info(response)
        
        return 1
    except RuntimeError:
        error_message = "Please refresh the website.\nThere is an error due to an interrupted server connection."
        logging.error("Failed to establish connection .")
        st.warning(f':red[{error_message}]')
        return None

# function to resize the image and display.
def image_displayer(image):
    img= Image.open(image)  # Open the image if it's uploaded
    width,heigth=img.size
    # resize the image 
    if width/heigth>0 and width-heigth<100:
        img=img.resize((300,250))
    elif width/heigth >0 and width-heigth>100:
        img=img.resize((350,250))
    elif width/heigth==1:
        img=img.resize((300,300))
    elif heigth/width>0 and heigth-width>100:
        img=img.resize((250,350))
    else:
        img=img.resize((250,300))
    st.image(img)
    
# function to catch empty columns and through a message to fill it.
def print_error_messages_if_empty(value_dict):
    for key, value in value_dict.items():
        if not value:
            st.warning(f":red[Please provide {key}.]")     
            
# Function to load the models. 
@st.cache_resource(show_spinner=False)
def model_loader():
    try:
        logging.info("model_loader called.")
        logging.info("Loading Blip Model.")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        logging.info("Blip Model loaded.")
        
        logging.info("Loading falcon.")
        falcon_model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin",)
        if falcon_model is None:
            logging.info("failed to load falcon")
            st.warning(":red[Please refresh the website.]")
        logging.info("Falcon Loaded.")
        return processor,model,falcon_model
        
    
    
    except:
        logging.warning("Problem while Loading Model")
        

    
    
