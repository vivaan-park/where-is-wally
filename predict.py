# © 2021 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

from utils.params import *
from utils.tiramisu import *

import numpy as np
from PIL import Image

from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.losses import categorical_crossentropy

def img_resize(img):
    h, w, _ = img.shape
    nvpanels = h / 224
    nhpanels = w / 224
    new_h, new_w = h, w
    if nvpanels * 224 != h:
        new_h = int((nvpanels + 1) * 224)
    if nhpanels * 224 != w:
        new_w = int((nhpanels + 1) * 224)
    if new_h == h and new_w == w:
        return img
    else:
        return (np.array(Image.fromarray(img).resize((new_h, new_w))) \
                / 255. - mu) / std

def split_panels(img):
    h, w, _ = img.shape
    num_vert_panels = int(h / 224)
    num_hor_panels = int(w / 224)
    panels = []
    for i in range(num_vert_panels):
        for j in range(num_hor_panels):
            panels.append(img[i*224:(i+1)*224, j*224:(j+1)*224])
    return np.stack(panels)

def combine_panels(img, panels):
    h, w, _ = img.shape
    num_vert_panels = int(h / 224)
    num_hor_panels = int(w / 224)
    total = []
    p = 0
    for i in range(num_vert_panels):
        row = []
        for j in range(num_hor_panels):
            row.append(panels[p])
            p += 1
        total.append(np.concatenate(row, axis=1))
    return np.concatenate(total, axis=0)

def reshape_pred(pred): return pred.reshape(224, 224, 2)[:,:,1]

def prediction_mask(img, target):
    layer1 = Image.fromarray(((img * std + mu) * 255).astype('uint8'))
    layer2 = Image.fromarray(
        np.concatenate(
            4 * [np.expand_dims(
                (225 * (1 - target)).astype('uint8'), axis=-1
            )], axis=-1
        )
    )
    result = Image.new('RGBA', layer1.size)
    result = Image.alpha_composite(result, layer1.convert('RGBA'))
    return Image.alpha_composite(result, layer2)
