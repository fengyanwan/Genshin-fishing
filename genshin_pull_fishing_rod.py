# coding: utf-8
import time

import cv2
import numpy as np
import win32api
import win32con
from PIL import ImageGrab

screen_center = (1920 // 2, 1080 // 2)
point_strategy = 1 / 2

bite_tip_area = (888, 203, 134, 24)
bite_tip_pic_path = 'picture\\bite_tip.png'
escape_tip_area = (801, 250, 318, 31)
escape_pic_path = 'picture\\escape_tip.png'

scroll_area = (710, 97, 500, 32)
cursor_pic_path = 'picture\\cursor.png'
left_endpoint_pic_path = 'picture\\left_endpoint.png'
right_endpoint_pic_path = 'picture\\right_endpoint.png'
cursor_img = cv2.imread(cursor_pic_path)
left_img = cv2.imread(left_endpoint_pic_path)
right_img = cv2.imread(right_endpoint_pic_path)

wait_display_time = 1
fish_catch = 0
fish_escape = 0


def is_tip_match(pic_path, region, shot_data=None, confidence=0.9):
    templ_pic = cv2.imread(pic_path)
    if shot_data is None:
        region_to_bbox = (region[0], region[1], region[0] + region[2], region[1] + region[3])
        shot_data = ImageGrab.grab(bbox=region_to_bbox)
        shot_data = np.asarray(shot_data)
        shot_data = cv2.cvtColor(shot_data, cv2.COLOR_RGB2BGR)
    match_result = cv2.matchTemplate(shot_data, templ_pic, cv2.TM_CCOEFF_NORMED)
    if match_result.max() >= confidence:
        return match_result.max()
    else:
        return False


def locate_pic_center(*img_tuple, region, shot_data=None, confidence=0.9):
    if shot_data is None:
        region_to_bbox = (region[0], region[1], region[0] + region[2], region[1] + region[3])
        screen_shot = ImageGrab.grab(bbox=region_to_bbox)
        shot_data = cv2.cvtColor(np.asarray(screen_shot), cv2.COLOR_RGB2BGR)
    match = []
    match_max = []
    dict_center = {}
    for img in img_tuple:
        result = cv2.matchTemplate(shot_data, img, cv2.TM_CCOEFF_NORMED)
        match.append(result)
        match_max.append(result.max())
    # print(match_max)
    for i in range(len(match_max)):
        if match_max[i] >= confidence:
            offset = np.unravel_index(match[i].argmax(), match[i].shape)
            center = (region[0] + offset[1] + img_tuple[i].shape[1] // 2,
                      region[1] + offset[0] + img_tuple[i].shape[0] // 2)
            dict_center[f'pic{i + 1}_center'] = center
        else:
            dict_center[f'pic{i + 1}_center'] = None
    return dict_center

    # --------------程序开始-------------#


if __name__ == '__main__':
    time.sleep(wait_display_time * 3)
    win32api.SetCursorPos(screen_center)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # loop 1 start
    while True:
        if is_tip_match(pic_path=bite_tip_pic_path, region=bite_tip_area):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(wait_display_time / 2)
            # loop 2 start
            while True:
                dict_xy = locate_pic_center(cursor_img,
                                            left_img,
                                            right_img,
                                            region=scroll_area,
                                            confidence=0.6)
                cursor_xy = dict_xy['pic1_center']
                left_xy = dict_xy['pic2_center']
                right_xy = dict_xy['pic3_center']
                if cursor_xy is None and left_xy is None and right_xy is None:
                    time.sleep(wait_display_time / 2)
                    dict_xy = locate_pic_center(cursor_img,
                                                left_img,
                                                right_img,
                                                region=scroll_area,
                                                confidence=0.6)
                    cursor_xy = dict_xy['pic1_center']
                    left_xy = dict_xy['pic2_center']
                    right_xy = dict_xy['pic3_center']
                    if cursor_xy is None and left_xy is None and right_xy is None:
                        if is_tip_match(pic_path=escape_pic_path, region=escape_tip_area):
                            fish_escape += 1
                            head = f'[{fish_catch}:{fish_escape}]'
                            print(f'{head} {fish_escape} fish escaped')
                        else:
                            fish_catch += 1
                            head = f'[{fish_catch}:{fish_escape}]'
                            print(f'{head} {fish_catch} fish caught')
                        time.sleep(wait_display_time * 3)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                        break
                if None in dict_xy.values():
                    continue
                judgement_point_x = left_xy[0] + (right_xy[0] - left_xy[0]) * point_strategy
                distance = judgement_point_x - cursor_xy[0]
                if distance >= 0:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    time.sleep(0.0035 * distance)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            # loop 2 end
        time.sleep(wait_display_time / 1.2)
    # loop 1 end
