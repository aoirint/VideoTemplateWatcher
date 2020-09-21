import sys
import cv2
import time
from pathlib import Path
from tqdm import tqdm
import yaml

import traceback
import inspect
import dataclasses as dcl
import typing
from typing import Tuple, List, Dict, Type

from VideoLoader import *
from FrameClassifier import *
from CVUtil import *
from VideoSearcher import *


def dataclass_from_dict(cls: Type[dcl.dataclass], data_dict: Dict):
    class_dict = dict()
    for key, val in data_dict.items():
        child_class = cls.__dataclass_fields__[key].type
        child_class_origin = typing.get_origin(child_class)

        try:
            if child_class_origin is not None and issubclass(child_class_origin, (tuple, list)):
                actual_child_class = typing.get_args(child_class)[0]
                v = [ dataclass_from_dict(actual_child_class, _val) for _val in val ]
                class_dict[key] = tuple(v) if issubclass(child_class_origin, tuple) else v

            elif child_class_origin is None and issubclass(child_class, Path):
                class_dict[key] = config_dir / Path(val)

            elif inspect.isclass(child_class) and dcl.is_dataclass(child_class):
                class_dict[key] = dataclass_from_dict(child_class, val)

            else:
                class_dict[key] = data_dict[key]
        except Exception as err:
            traceback.print_exc()
            raise err

    return cls(**class_dict)

def get_loader(options):
    loader = None

    if options.video_url:
        loader = YouTubeLoader(options.video_url)

    elif options.video_file:
        loader = FileLoader(options.video_file)

    elif options.live_channel_id:
        if not options.youtube_api_key:
            raise Exception('YouTube API Key is Required')

        live_videos = YouTubeLiveVideoSearcher.search_live_videos(
            api_key=options.youtube_api_key,
            channel_id=options.live_channel_id
        )
        if not live_videos:
            raise Exception('No live video found')

        live_video = live_videos[0]
        live_video_id = live_video.video_id

        loader = YouTubeLoader(video_id=live_video_id)

    return loader

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--config', type=str, required=True)
    options, _ = p.parse_known_args()
    config_path = Path(options.config)
    config_dir = config_path.parent

    import configargparse
    p = configargparse.ArgumentParser(config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.add('-c', '--config', env_var='CONFIG_FILE', required=True, is_config_file=True)

    p.add('-u', '--video_url', type=str, env_var='VIDEO_URL')
    p.add('-f', '--video_file', type=str, env_var='VIDEO_FILE')
    p.add('-l', '--live_channel_id', type=str, env_var='LIVE_CHANNEL_ID')
    p.add('--youtube_api_key', type=str, env_var='YOUTUBE_API_KEY')

    p.add('--global_bbox', type=lambda s: BBox(**yaml.safe_load(s)))
    p.add('--classes', nargs='*', type=lambda s: dataclass_from_dict(FrameClass, yaml.safe_load(s)))

    options = p.parse_args()

    loader = get_loader(options)
    assert loader is not None

    global_bbox = options.global_bbox

    frame_size = global_bbox.size if global_bbox else loader.size
    frame_classes = options.classes or []

    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    consumer = cv2.VideoWriter(
        filename='output.mkv',
        fourcc=fourcc,
        fps=int(loader.framerate),
        frameSize=frame_size,
    )

    # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', (game_box.w, game_box.h))

    framenum = loader.framenum or None

    frame_index = 0
    for frame in tqdm(loader.iter(), total=framenum):
        if frame is None:
            time.sleep(0.01)
            continue

        if global_bbox:
            frame = frame[global_bbox.top:global_bbox.bottom, global_bbox.left:global_bbox.right]

        res = None
        for fclass in frame_classes:
            res = fclass.matches(frame)
            if res:
                break

        text = ''
        text += f'F={frame_index}'
        if res:
            text += f', {fclass.label}'
            text += f': {res.value})'

        frame = cvPutText(
            img=frame,
            text=text,
            org=(8, 8),
            color=(255, 0, 255),
        )

        if res:
            bbox = res.bbox
            cv2.rectangle(
                img=frame,
                pt1=( bbox.left, bbox.top ),
                pt2=( bbox.right, bbox.bottom ),
                color=(255, 0, 255),
                thickness=1,
            )

        consumer.write(frame)

        frame_index += 1

        # cv2.imshow('frame', frame)
        # cv2.waitKey(1)

    consumer.release()
    loader.release()
