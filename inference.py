import numpy as np
import cv2
from linefiller.trappedball_fill import trapped_ball_fill_multi, flood_fill_multi, mark_fill, build_fill_map, merge_fill, \
    show_fill_map
from linefiller.thinning import thinning
import time
from log.logger import logger
import argparse


def processing(image:np.ndarray)->np.ndarray:
    ret, binary = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)
    
    fills = []
    result = binary

    fill = trapped_ball_fill_multi(result, 3, method='max')
    fills += fill
    result = mark_fill(result, fill)

    fill = trapped_ball_fill_multi(result, 2, method='mean')
    fills += fill
    result = mark_fill(result, fill)

    fill = trapped_ball_fill_multi(result, 1, method='mean')
    fills += fill
    result = mark_fill(result, fill)

    fill = flood_fill_multi(result)
    fills += fill

    fillmap = build_fill_map(result, fills)
    fillmap = merge_fill(fillmap)
    return fillmap

def saveAll(fillmap:np.ndarray,PATH:str)->None:
    # color+undertone
    cv2.imwrite(PATH+'fills_merged.png', show_fill_map(fillmap))
    # undertone
    cv2.imwrite(PATH+'fills_merged_no_contour.png', show_fill_map(thinning(fillmap)))

def main()->None:
    parser = argparse.ArgumentParser(description="Line Filler")
    # args
    parser.add_argument("-im","--image",type=str,help="Image Path",default="example.png")
    parser.add_argument("-o","--output",type=str,help="Save Root Path", default="./")

    args = parser.parse_args()

    im = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    logger.info("Start!")
    start = time.time()
    fillmap = processing(image=im)
    saveAll(fillmap=fillmap,PATH=args.output)
    logger.info("All Finished...")
    logger.info(f"Total Running Time : {time.time() - start :.2f}sec")

if __name__ == "__main__":
    main()