import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import json
from PIL import Image
from src.interrogator import WaifuDiffusionInterrogator

def load_json(fn):
    with open(fn,"r") as f:
        return json.load(f)
    
def get_tags_from_interrogate(results,thresh:float=0.35):
    condition = lambda v: v>thresh
    filted = {k:v for k,v in results[1].items() if condition(v)}
    return sorted(filted.items(),key=lambda v:v[1],reverse=True)

class Tagger():
    def __init__(self,model_name="wd14-vit-v2" ) -> None:
        self.tagger_dict = load_json("wd.json")
        self.interrogator = WaifuDiffusionInterrogator(model_name,repo_id=self.tagger_dict[model_name]["repo_id"])

    def tag(self,img:Image,thresh:float=0.35):
        results = self.interrogator.interrogate(img)
        return get_tags_from_interrogate(results,thresh=thresh)
    
    def tag_fn(self,fn:str,thresh:float=0.35):
        img = Image.open(fn)
        return self.tag(img)
    
    def print_tags(results=[]):
        for k,v in results:
            print(f"{k:>20}:{v:{10}.{3}}")

def test():
    tagger = Tagger()
    img = Image.open("./sample.png")
    results = tagger.tag(img)
    Tagger.print_tags(results)

def cli():
    tagger = Tagger()
    file_path = input("Image File:")
    results = tagger.tag_fn(file_path)
    Tagger.print_tags(results)

if __name__ == "__main__":
    #test()
    cli()