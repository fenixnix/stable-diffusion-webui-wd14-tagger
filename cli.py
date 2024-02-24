import json
from PIL import Image
from tagger.interrogator import WaifuDiffusionInterrogator

def load_json(fn):
    with open(fn,"r") as f:
        return json.load(f)
    
def get_tags_from_interrogate(results,thresh:float=0.35):
    condition = lambda v: v>thresh
    filted = {k:v for k,v in results[1].items() if condition(v)}
    return sorted(filted.items(),key=lambda v:v[1],reverse=True)

def init(default_tagger = "wd14-vit-v2"):
    tagger_dict = load_json("wd.json")
    return WaifuDiffusionInterrogator(default_tagger,repo_id=tagger_dict[default_tagger]["repo_id"])

def cli():
    tagger = init()

    img = Image.open("./sample.png")

    results = tagger.interrogate(img) # results[0] 统计，results[1] 细节

    for k,v in get_tags_from_interrogate(results):
        print(f"{k:>20}:{v:{10}.{3}}")

if __name__ == "__main__":
    cli()