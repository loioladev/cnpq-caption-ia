import json



path = '/media/matheus/Game/College/datasets/COCO2017/coco_ann2017/annotations'
with open(f'{path}/instances_val2017.json') as f:
    data = json.load(f)

