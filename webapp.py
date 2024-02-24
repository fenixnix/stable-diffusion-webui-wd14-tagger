import io
import os
from PIL import Image
import streamlit as st
from tagger import Tagger

def file2pilImage(st_file):
    return Image.open(io.BytesIO(st_file.read()))

if not "tagger" in st.session_state:
    st.session_state.tagger = Tagger()
    
anime = "👈👆🖕☝️👉👇"

tab1,tab2 = st.tabs(["图片处理","目录批量处理"])

with tab1:
    image_list = st.file_uploader("Choose some image",accept_multiple_files=True,type=["jpg","jpeg","png","webp"])
    threshold_tag1 = st.slider("阈值",0.1,1.0,0.35,key="tab1")
    if len(image_list)>0:
        bar = st.progress(0)
        st.image(image_list)


        with st.sidebar:
            for i in range(len(image_list)):
                img = file2pilImage(image_list[i])
                results = st.session_state.tagger.tag(img,threshold_tag1)
                bar.progress((1+i)/len(image_list),anime[i%len(anime)])
                for i in results: 
                    st.progress(i[1],i[0])
                st.markdown("-"*5)

with tab2:
    threshold_tag2 = st.slider("阈值",0.1,1.0,0.35,key="tab2")
    path = st.text_input("输入文件夹路径",value="D:/cover_output/")
    if st.button("处理"):
        img_tags = []
        for p,_,files in os.walk(path):
            for f in files:
                if f.split('.')[-1].lower() in ["webp","png","jpg","jpeg"]:
                    base_name = ".".join(f.split('.')[:-1])
                    img_fn = os.path.join(p,f)
                    tag_fn = os.path.join(p,base_name+".txt")
                    img_tags.append((img_fn,tag_fn))
        idx = 0
        bar = st.progress(0,f"[{idx}/{len(img_tags)}]")
        for img_fn,tag_fn in img_tags:
            idx += 1
            if os.path.exists(tag_fn):
                continue
            results = st.session_state.tagger.tag_fn(img_fn,threshold_tag2)
            textlist = []
            for name,pos in results:
                textlist.append(name)
            text = ", ".join(textlist)
            with open(tag_fn,"w",encoding="utf-8") as tag_file:
                tag_file.write(text)
            st.write(img_fn)
            st.markdown(f"`{text}`")
            bar.progress((idx)/len(img_tags),f"[{idx}/{len(img_tags)}]")
            