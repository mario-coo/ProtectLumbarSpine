#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProtectingLumbarSpine - 开放灶台双视窗动态仿真生成器 (V2 极致精修版)
左侧：全身解剖级动力学视窗（弯腰切菜、左腾右挪转腰、踩脚凳减压真实动作与脊柱应力）
右侧：L5/S1 椎间盘横断面微观病理视窗（流体髓核外突、纤维环拧毛巾剪切、S1神经根嵌顿放电）
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD_PATH = "C:/Windows/Fonts/msyhbd.ttc"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = FONT_PATH

FONT_TITLE = ImageFont.truetype(FONT_BOLD_PATH, 16)
FONT_SUB = ImageFont.truetype(FONT_PATH, 13)
FONT_CARD_TITLE = ImageFont.truetype(FONT_BOLD_PATH, 14)
FONT_BADGE = ImageFont.truetype(FONT_BOLD_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 11)
FONT_TINY = ImageFont.truetype(FONT_PATH, 10)
FONT_ALERT = ImageFont.truetype(FONT_BOLD_PATH, 11)

AXIAL_BASE_PATH = r"C:\Users\Administrator\.gemini\antigravity-ide\brain\6e0c6eac-6e3a-4675-b0d6-b33b30b16601\l5s1_axial_clean_rotation_1789892944925.jpg"
VIDEO_DIR = "media/video"
os.makedirs(VIDEO_DIR, exist_ok=True)


def draw_capsule(draw, p1, p2, radius, fill, outline=None, width=1):
    """绘制圆角胶囊肢体（大腿、小腿、手臂、躯干骨架）"""
    x1, y1 = p1
    x2, y2 = p2
    draw.line([p1, p2], fill=fill, width=int(radius * 2))
    draw.ellipse([(x1 - radius, y1 - radius), (x1 + radius, y1 + radius)], fill=fill)
    draw.ellipse([(x2 - radius, y2 - radius), (x2 + radius, y2 + radius)], fill=fill)
    if outline:
        draw.line([p1, p2], fill=outline, width=width)


def draw_lightning(draw, x1, y1, x2, y2, color=(255, 240, 50, 255), width=2, segments=4):
    """绘制神经电击放电折线"""
    dx = (x2 - x1) / segments
    dy = (y2 - y1) / segments
    pts = [(x1, y1)]
    for s in range(1, segments):
        offset = (6 if s % 2 == 1 else -6)
        px = x1 + dx * s - dy * 0.3 * (offset / 6.0)
        py = y1 + dy * s + dx * 0.3 * (offset / 6.0)
        pts.append((px, py))
    pts.append((x2, y2))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


def draw_text_badge(draw, x, y, text, font=FONT_SMALL, fill=(10, 16, 26, 220), outline=(0, 180, 240, 200), text_color=(240, 245, 255)):
    """绘制带背景防溢出的高清晰文字胶囊卡片"""
    bbox = font.getbbox(text)
    bw, bh = bbox[2] - bbox[0] + 12, bbox[3] - bbox[1] + 8
    draw.rounded_rectangle([(x, y), (x + bw, y + bh)], radius=4, fill=fill, outline=outline, width=1)
    draw.text((x + 6, y + 3), text, font=font, fill=text_color)
    return bw, bh


def render_left_viewport(w, h, prog_flex, prog_twist, prog_relief, frame_idx):
    """
    渲染左侧视窗：开放灶台解剖级全身动作与动力学
    包含：灶台、砧板、菜刀剁切动画、人物解剖肌群前屈、左腾右挪转腰、踩脚凳减压
    """
    im = Image.new("RGBA", (w, h), (10, 15, 22, 255))
    draw = ImageDraw.Draw(im)

    # 1. 视窗网格与环境底色
    for gx in range(0, w, 40):
        draw.line([(gx, 0), (gx, h)], fill=(18, 25, 36, 120), width=1)
    for gy in range(0, h, 40):
        draw.line([(0, gy), (w, gy)], fill=(18, 25, 36, 120), width=1)

    floor_y = 425

    # 地面阴影与踢脚线
    draw.line([(0, floor_y), (w, floor_y)], fill=(50, 70, 95, 200), width=2)
    draw.rectangle([(0, floor_y), (w, h)], fill=(12, 16, 24, 255))

    # 2. 现代开放式岛台 / 橱柜
    counter_x = 20
    counter_w = 175
    counter_top_y = 285  # 标准低台面 82cm
    # 柜体
    draw.rectangle([(counter_x, counter_top_y), (counter_x + counter_w, floor_y)], fill=(28, 38, 52, 255), outline=(55, 75, 100, 255), width=2)
    # 柜门抽屉分割线
    draw.line([(counter_x + 10, counter_top_y + 40), (counter_x + counter_w - 10, counter_top_y + 40)], fill=(45, 60, 80, 255), width=2)
    draw.line([(counter_x + 10, counter_top_y + 85), (counter_x + counter_w - 10, counter_top_y + 85)], fill=(45, 60, 80, 255), width=2)
    # 踢脚线凹槽 (Toe Kick)
    draw.rectangle([(counter_x + counter_w - 22, floor_y - 28), (counter_x + counter_w, floor_y)], fill=(14, 18, 26, 255))
    # 石英石台面边沿
    draw.rectangle([(counter_x - 5, counter_top_y - 8), (counter_x + counter_w + 6, counter_top_y)], fill=(55, 72, 94, 255), outline=(90, 120, 155, 255), width=1)

    # 3. 砧板系统（第四阶段自动垫高）
    if prog_relief > 0.05:
        # 垫高 10cm 实木加厚砧板 (厚度 34px)
        board_h = int(10 + 24 * prog_relief)
        board_top_y = counter_top_y - 8 - board_h
        draw.rectangle([(counter_x + 35, board_top_y), (counter_x + 160, counter_top_y - 8)], fill=(160, 105, 55, 255), outline=(220, 160, 95, 255), width=2)
        draw_text_badge(draw, counter_x + 40, board_top_y - 20, "加厚砧板 (+10cm)", font=FONT_TINY, fill=(35, 22, 12, 220), outline=(220, 150, 80, 220), text_color=(255, 230, 190))
    else:
        # 普通低矮薄砧板 (厚度 8px)
        board_h = 8
        board_top_y = counter_top_y - 8 - board_h
        draw.rectangle([(counter_x + 40, board_top_y), (counter_x + 155, counter_top_y - 8)], fill=(115, 75, 40, 255), outline=(145, 95, 55, 255), width=1)
        draw_text_badge(draw, counter_x + 40, board_top_y - 20, "普通低位薄砧板", font=FONT_TINY, fill=(30, 20, 15, 220), outline=(160, 100, 60, 200), text_color=(230, 190, 170))

    # 砧板上的蔬菜片 (胡萝卜片与青瓜片)
    draw.ellipse([(counter_x + 65, board_top_y - 4), (counter_x + 80, board_top_y + 1)], fill=(245, 105, 30, 255))
    draw.ellipse([(counter_x + 78, board_top_y - 4), (counter_x + 93, board_top_y + 1)], fill=(245, 115, 35, 255))
    draw.ellipse([(counter_x + 90, board_top_y - 4), (counter_x + 105, board_top_y + 1)], fill=(50, 180, 70, 255))

    # 4. 人体解剖动力学运动学 (Human Kinematics)
    base_hip_x = 295
    base_hip_y = 295

    # 左腾右挪横向平移与扭腰重心偏移
    sway_x = math.sin(prog_twist * math.pi * 2) * 22 if prog_twist > 0 else 0
    hip_x = base_hip_x + sway_x - prog_flex * 10 + prog_relief * (-28)  # 第四阶段腹部贴紧橱柜边缘借力
    hip_y = base_hip_y

    # 前屈角度 (0° ~ 28°)
    flex_deg = 28.0 * prog_flex * (1.0 - 0.85 * prog_relief)
    flex_rad = math.radians(flex_deg)

    # 躯干长轴与头部定位
    torso_len = 112
    chest_x = hip_x - math.sin(flex_rad) * (torso_len * 0.7)
    chest_y = hip_y - math.cos(flex_rad) * (torso_len * 0.7)

    head_x = hip_x - math.sin(flex_rad) * torso_len - 14 * prog_flex
    head_y = hip_y - math.cos(flex_rad) * torso_len - 8 * (1.0 - prog_flex)

    # 5. 绘制下肢解剖轮廓与 12cm 踩脚凳
    foot_r_x = base_hip_x + 18
    foot_r_y = floor_y - 10
    knee_r_x = (hip_x + foot_r_x) // 2 + 6
    knee_r_y = (hip_y + foot_r_y) // 2
    # 右腿（支撑腿，大腿与小腿胶囊体）
    draw_capsule(draw, (hip_x + 10, hip_y + 12), (knee_r_x, knee_r_y), 11, fill=(55, 70, 95, 255))
    draw_capsule(draw, (knee_r_x, knee_r_y), (foot_r_x, foot_r_y), 9, fill=(50, 65, 88, 255))
    draw.ellipse([(foot_r_x - 12, foot_r_y - 5), (foot_r_x + 18, foot_r_y + 8)], fill=(32, 42, 58, 255))

    # 左腿（前屈时平放，第四阶段踏上 12cm 防滑踩脚凳）
    if prog_relief > 0.05:
        # 12cm 实木防滑踩脚凳 (宽 65px, 高 38px)
        stool_x = counter_x + counter_w + 6
        stool_w = 64
        stool_h = 36
        stool_y = floor_y - stool_h
        draw.rounded_rectangle([(stool_x, stool_y), (stool_x + stool_w, floor_y)], radius=4, fill=(155, 100, 50, 255), outline=(225, 165, 100, 255), width=2)
        # 防滑橡胶底脚
        draw.rectangle([(stool_x + 5, floor_y - 5), (stool_x + 15, floor_y)], fill=(25, 25, 25, 255))
        draw.rectangle([(stool_x + stool_w - 15, floor_y - 5), (stool_x + stool_w - 5, floor_y)], fill=(25, 25, 25, 255))
        draw_text_badge(draw, stool_x + 4, stool_y + 8, "12cm踏板", font=FONT_TINY, fill=(40, 25, 15, 220), outline=(210, 150, 90, 220), text_color=(255, 235, 190))

        # 左脚踏在凳上，髋膝关节屈曲 25°
        foot_l_x = stool_x + 30
        foot_l_y = stool_y - 6
        knee_l_x = hip_x - 24
        knee_l_y = hip_y + 55
        draw_capsule(draw, (hip_x - 8, hip_y + 12), (knee_l_x, knee_l_y), 12, fill=(65, 82, 110, 255))
        draw_capsule(draw, (knee_l_x, knee_l_y), (foot_l_x, foot_l_y), 10, fill=(60, 78, 105, 255))
        draw.ellipse([(foot_l_x - 14, foot_l_y - 5), (foot_l_x + 16, foot_l_y + 7)], fill=(38, 50, 68, 255))
    else:
        foot_l_x = base_hip_x - 12
        foot_l_y = floor_y - 10
        knee_l_x = (hip_x + foot_l_x) // 2 - 4
        knee_l_y = (hip_y + foot_l_y) // 2
        draw_capsule(draw, (hip_x - 8, hip_y + 12), (knee_l_x, knee_l_y), 12, fill=(65, 82, 110, 255))
        draw_capsule(draw, (knee_l_x, knee_l_y), (foot_l_x, foot_l_y), 10, fill=(60, 78, 105, 255))
        draw.ellipse([(foot_l_x - 14, foot_l_y - 5), (foot_l_x + 15, foot_l_y + 8)], fill=(38, 50, 68, 255))

    # 6. 躯干解剖形体（胸背阔肌与腹部轮廓）
    draw_capsule(draw, (hip_x, hip_y), (chest_x, chest_y), 24, fill=(52, 68, 92, 240))
    draw_capsule(draw, (chest_x, chest_y), (head_x, head_y + 15), 18, fill=(58, 76, 102, 240))

    # 7. 头部解剖轮廓与下颌
    draw.ellipse([(head_x - 16, head_y - 18), (head_x + 16, head_y + 18)], fill=(215, 185, 155, 255), outline=(165, 135, 105, 255), width=1)
    # 耳廓与发际线
    draw.arc([(head_x - 17, head_y - 19), (head_x + 17, head_y + 19)], start=120, end=330, fill=(70, 50, 35, 255), width=4)
    draw.ellipse([(head_x + 8, head_y - 2), (head_x + 14, head_y + 8)], fill=(205, 175, 145, 255))
    # 眼睛视线（前屈时直视切配板）
    eye_x = head_x - 9
    eye_y = head_y - 2
    draw.ellipse([(eye_x - 2, eye_y - 2), (eye_x + 2, eye_y + 2)], fill=(35, 25, 15, 255))

    # 8. 脊柱骨链椎体（L1-L5，S1，胸椎骨块）
    num_vertebrae = 9
    spine_pts = []
    for vi in range(num_vertebrae):
        t = vi / (num_vertebrae - 1)
        arch = math.sin(t * math.pi) * (20 * prog_flex)
        vx = hip_x - math.sin(flex_rad) * (torso_len * t) - arch
        vy = hip_y - math.cos(flex_rad) * (torso_len * t)
        spine_pts.append((vx, vy))

    # 绘制高科技青白色脊柱骨链
    for vi in range(len(spine_pts) - 1):
        p1 = spine_pts[vi]
        p2 = spine_pts[vi + 1]
        draw.line([p1, p2], fill=(160, 220, 255, 160), width=4)
        draw.ellipse([(p1[0] - 3, p1[1] - 3), (p1[0] + 3, p1[1] + 3)], fill=(220, 245, 255, 220))

    # 9. L5/S1 重点应力警报与光斑 (位于底部 t=0~2 处)
    l5s1_x, l5s1_y = spine_pts[1]

    if prog_relief > 0.3:
        # 科学减压：健康青绿色柔和光芒
        draw.ellipse([(l5s1_x - 16, l5s1_y - 16), (l5s1_x + 16, l5s1_y + 16)], fill=(40, 220, 120, 90))
        draw.ellipse([(l5s1_x - 7, l5s1_y - 7), (l5s1_x + 7, l5s1_y + 7)], fill=(120, 255, 180, 255))
        draw_text_badge(draw, l5s1_x + 20, l5s1_y - 12, "L5/S1: 1120N (减压)", font=FONT_SMALL, fill=(12, 28, 20, 220), outline=(50, 220, 120, 220), text_color=(140, 255, 180))
    elif prog_twist > 0.1:
        # 左腾右挪转腰剪切：爆燃红黄色电火花高危警报
        pulse = math.sin(frame_idx * 0.8) * 8
        glow_r = int(24 + pulse)
        draw.ellipse([(l5s1_x - glow_r, l5s1_y - glow_r), (l5s1_x + glow_r, l5s1_y + glow_r)], fill=(255, 40, 40, 150))
        draw.ellipse([(l5s1_x - 10, l5s1_y - 10), (l5s1_x + 10, l5s1_y + 10)], fill=(255, 230, 50, 255))
        # 旋转扭矩破坏弧线
        draw.arc([(l5s1_x - 30, l5s1_y - 30), (l5s1_x + 30, l5s1_y + 30)], start=30, end=210, fill=(255, 60, 60, 255), width=3)
        draw_text_badge(draw, l5s1_x + 22, l5s1_y - 20, "【警报】转腰剪切350%", font=FONT_ALERT, fill=(45, 12, 12, 230), outline=(255, 60, 60, 240), text_color=(255, 90, 80))
        draw_text_badge(draw, l5s1_x + 22, l5s1_y + 4, "3100N 暴力超载", font=FONT_SMALL, fill=(35, 20, 10, 220), outline=(255, 160, 50, 220), text_color=(255, 200, 100))
    elif prog_flex > 0.15:
        # 前屈深躬：血红高压红斑
        pulse = math.sin(frame_idx * 0.5) * 5
        glow_r = int(18 + pulse)
        draw.ellipse([(l5s1_x - glow_r, l5s1_y - glow_r), (l5s1_x + glow_r, l5s1_y + glow_r)], fill=(255, 50, 50, 140))
        draw.ellipse([(l5s1_x - 7, l5s1_y - 7), (l5s1_x + 7, l5s1_y + 7)], fill=(255, 180, 50, 255))
        draw_text_badge(draw, l5s1_x + 22, l5s1_y - 16, "【警报】暴压 2520N", font=FONT_ALERT, fill=(45, 12, 12, 230), outline=(255, 60, 60, 240), text_color=(255, 90, 80))
        draw_text_badge(draw, l5s1_x + 22, l5s1_y + 8, "前屈长悬臂重载", font=FONT_SMALL, fill=(35, 18, 15, 220), outline=(255, 120, 80, 200), text_color=(255, 180, 140))
    else:
        # 初始中立
        draw.ellipse([(l5s1_x - 6, l5s1_y - 6), (l5s1_x + 6, l5s1_y + 6)], fill=(0, 200, 255, 255))
        draw_text_badge(draw, l5s1_x + 20, l5s1_y - 8, "L5/S1基线: 850N", font=FONT_SMALL, fill=(10, 20, 32, 220), outline=(0, 180, 240, 200), text_color=(180, 220, 255))

    # 10. 双臂动作与动态切菜菜刀 (Chopping Knife Motion)
    shoulder_x = chest_x - 6
    shoulder_y = chest_y + 10

    # 菜刀快速起伏频率（弯腰切菜与减压切菜时连续起伏）
    is_chopping = (prog_flex > 0.1 or prog_relief > 0.1)
    chop_motion = abs(math.sin(frame_idx * 0.9)) * 15 if is_chopping else 2
    knife_edge_y = board_top_y - chop_motion
    knife_x = counter_x + 100

    # 右臂（握刀臂，上臂与前臂关节联动）
    hand_x = knife_x + 25
    hand_y = knife_edge_y - 8
    elbow_x = shoulder_x - 18 + prog_flex * 12
    elbow_y = (shoulder_y + hand_y) // 2 + 10
    draw_capsule(draw, (shoulder_x, shoulder_y), (elbow_x, elbow_y), 9, fill=(65, 82, 110, 255))
    draw_capsule(draw, (elbow_x, elbow_y), (hand_x, hand_y), 7, fill=(65, 82, 110, 255))

    # 钢制菜刀刀身与木柄
    draw.polygon([(knife_x - 32, knife_edge_y - 20), (knife_x + 22, knife_edge_y - 20), (knife_x + 22, knife_edge_y), (knife_x - 32, knife_edge_y)], fill=(225, 235, 245, 255), outline=(150, 175, 200, 255))
    draw.rectangle([(knife_x + 20, knife_edge_y - 18), (knife_x + 38, knife_edge_y - 9)], fill=(95, 52, 28, 255))
    # 菜刀下切撞击高亮线
    if chop_motion < 4:
        draw.line([(knife_x - 34, board_top_y + 1), (knife_x + 24, board_top_y + 1)], fill=(255, 255, 255, 240), width=2)

    # 左臂（扶菜臂）
    left_hand_x = counter_x + 68
    left_hand_y = board_top_y - 4
    draw_capsule(draw, (shoulder_x, shoulder_y), (left_hand_x + 12, left_hand_y - 18), 8, fill=(52, 68, 92, 255))
    draw_capsule(draw, (left_hand_x + 12, left_hand_y - 18), (left_hand_x, left_hand_y), 7, fill=(52, 68, 92, 255))

    return im


def render_right_viewport(w, h, base_roi, prog_flex, prog_twist, prog_relief, frame_idx):
    """
    渲染右侧视窗：L5/S1 椎间盘横断面微观病理与神经挤压联动
    包含：流体髓核后移突出、纤维环拧毛巾剪切撕裂、右侧 S1 神经根受压与电击放电
    """
    im = base_roi.copy()
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 关键解剖坐标：
    nuc_cx, nuc_cy = 230, 300
    prot_cx, prot_cy = 345, 220
    nerve_cx, nerve_cy = 385, 200
    facet_cx, facet_cy = 365, 115

    # 1. 动态流体髓核外突形变 (Nucleus Pulposus Extrusion)
    if prog_relief > 0.2:
        # 阶段四：减压回纳平复
        cur_depth = round(6.5 - 0.9 * prog_relief, 1)
        ext_r = int(18 - 8 * prog_relief)
        draw.ellipse([(prot_cx - ext_r, prot_cy - ext_r), (prot_cx + ext_r, prot_cy + ext_r)], fill=(100, 210, 255, 90), outline=(0, 220, 255, 180), width=1)
        draw_text_badge(draw, prot_cx - 50, prot_cy - 40, f"突出回纳: {cur_depth}mm", font=FONT_TINY, fill=(10, 25, 20, 220), outline=(60, 220, 130, 200), text_color=(130, 255, 180))
    elif prog_twist > 0.1:
        # 阶段三：转腰剪切挤压峰值 (6.7mm)
        pulse = math.sin(frame_idx * 0.9) * 3
        ext_r = int(28 + pulse)
        cur_depth = round(6.3 + 0.4 * prog_twist, 1)
        draw.ellipse([(prot_cx - ext_r, prot_cy - ext_r), (prot_cx + ext_r, prot_cy + ext_r)], fill=(255, 50, 50, 160), outline=(255, 220, 50, 240), width=2)
        draw_text_badge(draw, prot_cx - 55, prot_cy - 44, f"【警报】剪切暴突 {cur_depth}mm", font=FONT_TINY, fill=(45, 10, 10, 230), outline=(255, 60, 60, 240), text_color=(255, 80, 80))
    elif prog_flex > 0.1:
        # 阶段二：前屈挤压外突 (5.6mm ➔ 6.3mm)
        ext_r = int(14 + 12 * prog_flex)
        cur_depth = round(5.6 + 0.7 * prog_flex, 1)
        draw.ellipse([(prot_cx - ext_r, prot_cy - ext_r), (prot_cx + ext_r, prot_cy + ext_r)], fill=(240, 70, 50, 130), outline=(255, 100, 70, 220), width=2)
        draw_text_badge(draw, prot_cx - 50, prot_cy - 40, f"流体髓核外突 {cur_depth}mm", font=FONT_TINY, fill=(40, 15, 10, 220), outline=(255, 110, 70, 220), text_color=(255, 160, 110))
    else:
        # 阶段一：基线
        draw.ellipse([(prot_cx - 12, prot_cy - 12), (prot_cx + 12, prot_cy + 12)], fill=(0, 180, 240, 80), outline=(0, 200, 255, 160), width=1)
        draw_text_badge(draw, prot_cx - 45, prot_cy - 34, "基线突出: 5.6mm", font=FONT_TINY, fill=(10, 20, 30, 220), outline=(0, 180, 240, 180), text_color=(180, 220, 255))

    # 2. 纤维环同心层间剪切线 (Annulus Fibrosus Torsion Shear)
    if prog_twist > 0.15:
        # 扭转时纤维环板层交错剪应力激增
        for r_ring in [45, 65, 85]:
            draw.arc([(nuc_cx - r_ring, nuc_cy - r_ring * 0.6), (nuc_cx + r_ring, nuc_cy + r_ring * 0.6)], start=10, end=190, fill=(255, 60, 60, 200), width=2)
        draw_text_badge(draw, nuc_cx - 85, nuc_cy + 35, "纤维环拧毛巾剪切破坏(350%)", font=FONT_TINY, fill=(40, 10, 10, 220), outline=(255, 60, 60, 220), text_color=(255, 100, 100))

    # 3. 右侧 S1 神经根受压与电击放电 (Right S1 Nerve Root)
    if prog_relief > 0.3:
        # 减压通畅：健康圆润形态 + 绿色光晕
        draw.ellipse([(nerve_cx - 12, nerve_cy - 12), (nerve_cx + 12, nerve_cy + 12)], fill=(40, 200, 100, 200), outline=(100, 255, 160, 255), width=2)
        draw_text_badge(draw, nerve_cx - 20, nerve_cy + 18, "S1 神经供血恢复", font=FONT_TINY, fill=(10, 30, 18, 220), outline=(60, 220, 120, 220), text_color=(120, 255, 160))
    elif prog_twist > 0.15:
        # 转腰重度绞杀：神经压扁 75% + 剧烈电火花放电
        draw.ellipse([(nerve_cx - 16, nerve_cy - 6), (nerve_cx + 16, nerve_cy + 6)], fill=(255, 20, 20, 240), outline=(255, 240, 50, 255), width=2)
        # 放电折线
        for ang in range(0, 360, 45):
            rad = math.radians(ang + (frame_idx * 35) % 360)
            ex1 = nerve_cx + math.cos(rad) * 10
            ey1 = nerve_cy + math.sin(rad) * 6
            ex2 = nerve_cx + math.cos(rad) * 26
            ey2 = nerve_cy + math.sin(rad) * 20
            draw_lightning(draw, ex1, ey1, ex2, ey2, color=(255, 240, 60, 240), width=2)
        draw_text_badge(draw, nerve_cx - 30, nerve_cy + 22, "【警报】神经压扁75%剧痛放电", font=FONT_TINY, fill=(45, 10, 10, 240), outline=(255, 50, 50, 240), text_color=(255, 70, 70))
    elif prog_flex > 0.15:
        # 前屈卡压：变形 40% + 局部充血
        draw.ellipse([(nerve_cx - 14, nerve_cy - 8), (nerve_cx + 14, nerve_cy + 8)], fill=(230, 40, 40, 220), outline=(255, 180, 50, 240), width=2)
        draw_text_badge(draw, nerve_cx - 20, nerve_cy + 18, "神经卡压充血", font=FONT_TINY, fill=(40, 12, 12, 220), outline=(255, 90, 70, 220), text_color=(255, 120, 90))
    else:
        # 基线轻度推挤
        draw.ellipse([(nerve_cx - 10, nerve_cy - 10), (nerve_cx + 10, nerve_cy + 10)], fill=(220, 80, 80, 180), outline=(255, 150, 150, 220), width=1)
        draw_text_badge(draw, nerve_cx - 15, nerve_cy + 16, "右侧 S1 神经", font=FONT_TINY, fill=(30, 15, 15, 220), outline=(220, 100, 100, 200), text_color=(240, 180, 180))

    # 4. 小关节撞击（转腰时触发）
    if prog_twist > 0.2:
        draw.ellipse([(facet_cx - 12, facet_cy - 12), (facet_cx + 12, facet_cy + 12)], fill=(255, 60, 60, 200))
        draw_text_badge(draw, facet_cx - 45, facet_cy - 24, "小关节撞击 850N", font=FONT_TINY, fill=(45, 15, 15, 220), outline=(255, 100, 80, 220), text_color=(255, 160, 120))

    # 5. 左侧通畅神经对照
    draw.ellipse([(115 - 10, 215 - 10), (115 + 10, 215 + 10)], fill=(80, 220, 120, 200), outline=(140, 255, 180, 220), width=1)
    draw_text_badge(draw, 80, 230, "左侧正常神经", font=FONT_TINY, fill=(10, 25, 15, 220), outline=(60, 200, 100, 200), text_color=(160, 255, 190))

    return Image.alpha_composite(im, overlay)


def build_coupled_dynamic_gif():
    """生成双视窗动作联动高清 GIF"""
    print("Loading axial base render...")
    raw_axial = Image.open(AXIAL_BASE_PATH).convert("RGBA")
    # 裁剪中心腰椎病理 ROI
    roi = raw_axial.crop((180, 80, 1020, 780))
    vp_w, vp_h = 465, 455
    axial_roi = roi.resize((vp_w, vp_h), Image.Resampling.LANCZOS)

    canvas_w, canvas_h = 1000, 660
    total_frames = 64
    frames = []

    print(f"Generating {total_frames} coupled animation frames...")

    for i in range(total_frames):
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (8, 12, 18, 255))
        cdraw = ImageDraw.Draw(canvas)

        # 阶段与动力学参数插值
        if i <= 11:
            phase_name = "【阶段一：中立准备工况】"
            action_desc = "躯干端正直立，双足平站，L5/S1 承受基础重力，椎间孔通畅"
            prog_flex = 0.0
            prog_twist = 0.0
            prog_relief = 0.0
            trunk_deg = "0.0° (直立)"
            twist_deg = "0.0° (未旋转)"
            disc_press = "850 N (基线)"
            disc_col = (80, 230, 120, 255)
            shear_val = "0% (生理平衡)"
            nerve_stat = "通畅 (无卡压，微循环良好)"
            nerve_col = (80, 230, 120, 255)
        elif i <= 27:
            p = (i - 11) / 16.0
            phase_name = "【阶段二：低台面深躬切配】"
            action_desc = f"躯干前屈弯腰 {p*28:.0f}°，菜刀连续下切；长悬臂重载迫使髓核后移，L5/S1 暴压"
            prog_flex = p
            prog_twist = 0.0
            prog_relief = 0.0
            trunk_deg = f"{p*28:.1f}° (深躬前倾)"
            twist_deg = "0.0°"
            disc_press = f"{int(850 + 1670*p)} N (超载暴增)"
            disc_col = (255, 120 - int(40*p), 50, 255)
            shear_val = "45% (开始前倾受拉)"
            nerve_stat = f"卡压加剧 (变形率 {int(20+35*p)}%)"
            nerve_col = (255, 120, 80, 255)
        elif i <= 43:
            p = (i - 27) / 16.0
            prog_flex = 1.0
            prog_twist = p
            prog_relief = 0.0
            cur_twist = round(p * 3.8, 1)
            phase_name = "【阶段三：左腾右挪 · 侧身转腰取物】"
            action_desc = f"前屈中强行扭腰 {cur_twist}°！突破小关节生理门闩，纤维环 350% 剪应力绞杀神经！"
            trunk_deg = "28.0° (持续前屈)"
            twist_deg = f"{cur_twist}° (超限死锁破坏)"
            disc_press = f"{int(2520 + 580*p)} N (峰值毁坏压)"
            disc_col = (255, 40, 40, 255)
            shear_val = f"{int(45 + 305*p)}% (50%纤维失效)"
            nerve_stat = "高危绞杀 (轴突高频剧痛放电)"
            nerve_col = (255, 40, 40, 255)
        else:
            p = (i - 43) / 20.0
            prog_flex = 1.0 - p * 0.85
            prog_twist = 0.0
            prog_relief = p
            cur_flex = round(28.0 * (1.0 - p * 0.85), 1)
            phase_name = "【阶段四：人体工学防护 · 踩脚凳+垫高砧板】"
            action_desc = "单脚踏入 12cm 踏板屈髋，砧板垫高 10cm，躯干直立归正，小腹靠台卸载 35%"
            trunk_deg = f"{cur_flex}° (中立微前倾)"
            twist_deg = "0.0° (严禁扭转)"
            disc_press = f"{int(3100 - 1980*p)} N (大减载)"
            disc_col = (70, 220, 130, 255)
            shear_val = "0% (剪切应力清零)"
            nerve_stat = "彻底释放 (右侧 S1 恢复血流通畅)"
            nerve_col = (70, 220, 130, 255)

        # 1. 顶部主面板 (Top HUD)
        cdraw.rounded_rectangle([(15, 8), (canvas_w - 15, 62)], radius=6, fill=(12, 18, 28, 240), outline=(0, 200, 255, 200), width=1)
        cdraw.text((25, 12), "【开放厨房动态姿态与 L5/S1 横断面受力联动仿真 (Kinematic & Axial Biomechanics)】", font=FONT_TITLE, fill=(0, 220, 255, 255))
        cdraw.text((25, 36), f"{phase_name} {action_desc}", font=FONT_SUB, fill=(215, 235, 255, 240))

        # 2. 渲染左侧视窗 (全身动作与脊柱受力)
        left_im = render_left_viewport(vp_w, vp_h, prog_flex, prog_twist, prog_relief, i)
        canvas.paste(left_im, (18, 72))
        cdraw.rounded_rectangle([(18, 72), (18 + vp_w, 72 + vp_h)], radius=6, outline=(0, 180, 240, 160), width=1)
        # 视窗标签
        cdraw.rounded_rectangle([(24, 76), (255, 98)], radius=4, fill=(10, 20, 30, 220))
        cdraw.text((30, 79), "【视窗 1：全身工效学姿态与动作】", font=FONT_BADGE, fill=(0, 210, 255, 255))

        # 3. 渲染右侧视窗 (L5/S1 椎间盘横断面病理)
        right_im = render_right_viewport(vp_w, vp_h, axial_roi, prog_flex, prog_twist, prog_relief, i)
        canvas.paste(right_im, (canvas_w - 18 - vp_w, 72))
        cdraw.rounded_rectangle([(canvas_w - 18 - vp_w, 72), (canvas_w - 18, 72 + vp_h)], radius=6, outline=(255, 100, 80, 180), width=1)
        # 视窗标签
        cdraw.rounded_rectangle([(canvas_w - 18 - vp_w + 6, 76), (canvas_w - 18 - vp_w + 265, 98)], radius=4, fill=(30, 15, 15, 220))
        cdraw.text((canvas_w - 18 - vp_w + 12, 79), "【视窗 2：L5/S1 轴位横断面受力病理】", font=FONT_BADGE, fill=(255, 130, 100, 255))

        # 4. 底部实时遥测数据看板 (Bottom Telemetry Dashboard)
        dash_y = 536
        dash_h = 115
        cdraw.rounded_rectangle([(15, dash_y), (canvas_w - 15, dash_y + dash_h)], radius=6, fill=(10, 15, 24, 245), outline=(0, 200, 255, 180), width=1)
        cdraw.text((25, dash_y + 8), "【脊柱生物力学与 S1 神经根实时遥测看板 (Real-Time Telemetry Dashboard)】", font=FONT_CARD_TITLE, fill=(0, 210, 255, 255))
        cdraw.line([(25, dash_y + 28), (canvas_w - 25, dash_y + 28)], fill=(0, 180, 240, 60), width=1)

        cols = [
            ("躯干前倾角", trunk_deg, (255, 220, 100, 255)),
            ("腰椎扭转角", twist_deg, (255, 140, 90, 255) if prog_twist > 0 else (120, 230, 140, 255)),
            ("L5/S1 轴向压力", disc_press, disc_col),
            ("纤维环剪切率", shear_val, (255, 70, 70, 255) if prog_twist > 0 else (180, 220, 240, 255)),
            ("右侧 S1 神经根", nerve_stat, nerve_col)
        ]
        cw = (canvas_w - 50) // len(cols)
        for col_idx, (c_label, c_val, c_color) in enumerate(cols):
            cx = 25 + col_idx * cw
            cdraw.text((cx, dash_y + 36), c_label, font=FONT_SMALL, fill=(180, 200, 220, 240))
            cdraw.text((cx, dash_y + 56), c_val, font=FONT_SMALL, fill=c_color)

        cdraw.text((25, dash_y + 88), "★ 核心临床铁律：灶台切菜弯腰 + 扭腰侧身取物是纤维环毁灭复合力矩！务必垂直垫高砧板 10cm + 12cm 踩脚凳交替卸载！", font=FONT_ALERT, fill=(255, 220, 120, 255))

        frames.append(canvas.convert("RGB"))

    out_gif = os.path.join(VIDEO_DIR, "axial_kitchen_flexion_dynamic.gif")
    print(f"Saving high-precision animated GIF to {out_gif}...")
    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=95,
        loop=0
    )
    print(f"Successfully generated dynamic coupled simulation GIF: {out_gif} ({len(frames)} frames, size: {os.path.getsize(out_gif)} bytes)")


if __name__ == "__main__":
    build_coupled_dynamic_gif()
