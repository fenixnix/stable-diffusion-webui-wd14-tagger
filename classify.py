from transformers import pipeline

pipe_aesthetic = pipeline("image-classification", "cafeai/cafe_aesthetic")
def aesthetic_classify(input_img):
    data = pipe_aesthetic(input_img, top_k=2)
    final = {}
    for d in data:
        final[d["label"]] = d["score"]
    return final

pipe_style = pipeline("image-classification", "cafeai/cafe_style")
def style_classify(input_img):
    data = pipe_style(input_img, top_k=5)
    final = {}
    for d in data:
        final[d["label"]] = d["score"]
    return final

pipe_waifu = pipeline("image-classification", "cafeai/cafe_waifu")
def waifu_classify(input_img):
    data = pipe_waifu(input_img, top_k=5)
    final = {}
    for d in data:
        final[d["label"]] = d["score"]
    return final