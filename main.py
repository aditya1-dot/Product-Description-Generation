import streamlit as st
from streamlit_flexselect import flexselect
import logging
from PIL import Image
from utils import generate_image_caption, generate_product_description, setup_logging,load_lottiefile,model_loader,print_error_messages_if_empty
from streamlit_lottie import st_lottie_spinner


def main():
    setup_logging()
    st.set_page_config(layout="wide")
    
    st.title("Product Description Generator")
    
    # Upload an image
    col1,col2=st.columns([2,3],gap="small")
    
    with col1:
        image_file = st.file_uploader("Upload an image :red[*]", type=["jpg", "jpeg", "png"],key="product_img")
        
        if image_file is not None:
            
            logging.info(f"Image uploaded: {image_file.name} ({image_file.type})")

        product_title=""
        product_title=st.text_input(label="Product Title :red[*]",max_chars=35,)
        brand = st.text_input(label="Brand",max_chars=25,label_visibility="visible",)
        brand='brand: '+brand
        options=[]
        key_feature = flexselect(
            label="Key Features",
            options=options
            )
        key_features=",".join(key_feature)

        selected_value = st.slider("Max Length for Description", min_value=50, max_value=200, value=50, step=25,help="Ensure that the maximum text length aligns with the key features provided to obtain results that are contextually relevant and meaningful.")
        button=st.button("SUBMIT")
        model_loader()
        if button:
            required_feild={"Image":image_file,
                            "Product Title":product_title}
            print_error_messages_if_empty(required_feild)
                
    # Get user input for brand and key features
    with col2:
        
        if button:
            if image_file  is not None and product_title!="":
                # logging all the inputs
                logging.info("generation initiated")
                logging.info(f'product_title:{product_title}')
                logging.info(f'brand:{brand}')
                logging.info(f'key_features:{key_features}')

                
                # a varibale for showing the process status to user
                global dy_text
                dy_text=st.empty()
                
                #Generating image caption 
                caption=""
                loading=load_lottiefile("/DesktopPROJECT/setmax/loop.json")
                with st_lottie_spinner(animation_source=loading,height=500,width=500,):
                    text="for sales!"
                    caption=generate_image_caption(image_path=image_file,text_to_condition=text)
                
                # generating product description 
                    # writing the prompt to be passed
                imp_prompt="do not repeat points and start with  key features as heading do not inculde model name or brand name in heading, also bold the points ."
                prompt = "write  key features of the product for selling on amazon ;in maximum limit of "
                prompt=prompt+str(selected_value)+" words :"+ " "+ str(caption)+" brand:"+brand+" product title:"+product_title+" key features:"+key_features+imp_prompt
                
                result=generate_product_description(prompt)
                # logging the termination status 
                if result :
                    logging.info("task completed\n")
                else:
                    logging.info("Task failed\n")
                    
                
            else:
                flag=12
    

if __name__ == "__main__":
    main()
