import io
from PIL import Image
from fastapi import FastAPI,UploadFile,File,Body

from classify import aesthetic_classify,style_classify,waifu_classify
from tagger import Tagger

from util import base64_to_image

app = FastAPI()

@app.get("/")
async def root():
    return {
        "msg":"tagger&classify"
    }

def classify_image(img:Image,model:str):
    print(f"{model = }")
    result = {}
    match model:
        case "aesthetic": result = aesthetic_classify(img)
        case "style": result = style_classify(img)
        case "waifu": result = waifu_classify(img)
        case _:print("model not found!")
    return {"result":result}

@app.post('/imagef/classify/{model}',tags=["classify"],description="Image Classify: aesthetic,style,waifu")
async def image_classify(model:str="aesthetic", file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    return classify_image(img,model)

@app.post('/imageb64/classify/{model}',tags=["classify"],description="Image Classify: aesthetic,style,waifu")
async def image_classify(model:str="aesthetic", imgb64=Body(...)):
    img = base64_to_image(imgb64)
    return classify_image(img,model)

tagger = Tagger()

@app.post('/imagef/tagger',tags=["tagger"],description="Image Tagger")
async def image_tagger(thresh:float=0.35,file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    print(f"{thresh = }")
    result = {}
    result = tagger.tag(img,thresh)
    return {"result":result}