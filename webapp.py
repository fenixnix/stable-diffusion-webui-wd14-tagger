import io
from PIL import Image
import streamlit as st

from tagger import Tagger

def file2pilImage(st_file):
    return Image.open(io.BytesIO(st_file.read()))

if not "tagger" in st.session_state:
    st.session_state.tagger = Tagger()


image_list = []

threshold = st.slider("阈值",0.0,1.0,0.35)
bar = st.progress(0)
    
image_list = st.file_uploader("Choose some image",accept_multiple_files=True,type=["jpg","jpeg","png","webp"])
st.image(image_list)
        
with st.sidebar:
    for i in range(len(image_list)):
        img = file2pilImage(image_list[i])
        results = st.session_state.tagger.tag(img,threshold)
        bar.progress((1+i)/len(image_list))
        for i in results: 
            st.progress(i[1],i[0])
        st.markdown("-"*5)
    