# © 2021 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

def extract_224_sub_image(img, box):
    wstart, wend, hstart, hend = box
    i = img[wend-224:wstart+224, hend-224:hstart+224]
    if not i.shape[0]:
        return img[wstart:wstart+225, hend-224:hstart+224]
    else:
        return i