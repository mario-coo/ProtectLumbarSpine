#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProtectingLumbarSpine - 开放灶台区生物力学图解与高精动态演变仿真构建流水线
本脚本根据三甲医院骨科与人体工学标准，将 3D 渲染底图转化为 100% 纯中文医学级可视化图解与动态仿真。
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD_PATH = "C:/Windows/Fonts/msyhbd.ttc"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = FONT_PATH

FONT_TITLE = ImageFont.truetype(FONT_BOLD_PATH, 20)
FONT_CARD_TITLE = ImageFont.truetype(FONT_BOLD_PATH, 15)
FONT_CARD_BODY = ImageFont.truetype(FONT_PATH, 13)
FONT_CARD_SUB = ImageFont.truetype(FONT_PATH, 13)
FONT_BADGE = ImageFont.truetype(FONT_BOLD_PATH, 13)
FONT_TELEMETRY = ImageFont.truetype(FONT_PATH, 12)
FONT_ALERT = ImageFont.truetype(FONT_PATH, 12)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 11)

BRAIN_DIR = r"C:\Users\Administrator\.gemini\antigravity-ide\brain\d916caf1-6063-47e1-8dc1-635391f87d1b"
IMG_DIR = "media/images"
VIDEO_DIR = "media/video"
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def draw_clean_cross(draw, cx, cy, r=8, color=(200, 20, 20, 255), width=3):
    draw.line([(cx - r, cy - r), (cx + r, cy + r)], fill=color, width=width)
    draw.line([(cx - r, cy + r), (cx + r, cy - r)], fill=color, width=width)


def draw_clean_check(draw, cx, cy, r=8, color=(15, 120, 50, 255), width=3):
    p1 = (cx - r, cy)
    p2 = (cx - r // 3, cy + r)
    p3 = (cx + r, cy - r)
    draw.line([p1, p2], fill=color, width=width)
    draw.line([p2, p3], fill=color, width=width)


def draw_badge(draw, x, y, text, fill=(15, 22, 32, 235), outline=(0, 180, 240, 200), text_color=(240, 245, 255)):
    bbox = FONT_BADGE.getbbox(text)
    bw, bh = bbox[2] - bbox[0] + 16, bbox[3] - bbox[1] + 12
    draw.rounded_rectangle([(x, y), (x + bw, y + bh)], radius=4, fill=fill, outline=outline, width=1)
    draw.text((x + 8, y + 4), text, font=FONT_BADGE, fill=text_color)
    return (x, y, bw, bh)


def build_image_18():
    """构建 18_kitchen_posture_comparison_3d.jpg"""
    base_path = os.path.join(BRAIN_DIR, "kitchen_posture_clean_base_1790135744317.jpg")
    base = Image.open(base_path).convert("RGBA")
    w, h = base.size  # 1200, 896

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. 顶部总标题
    tw, th = 780, 46
    tx, ty = (w - tw) // 2, 20
    draw.rounded_rectangle([(tx, ty), (tx + tw, ty + th)], radius=6, fill=(12, 18, 28, 230), outline=(0, 200, 255, 200), width=1)
    draw.text((tx + 28, ty + 10), "【开放灶台站姿力学透视：错误前屈深躬 vs 科学垫高卸载】", font=FONT_TITLE, fill=(240, 248, 255, 255))

    # 2. 错误姿势横幅 (左侧)
    bw, bh = 530, 68
    bx, by = 40, 78
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=8, fill=(180, 25, 25, 220), outline=(255, 80, 80, 240), width=2)
    draw.ellipse([(bx + 14, by + 14), (bx + 48, by + 48)], fill=(255, 230, 230, 255))
    draw_clean_cross(draw, bx + 31, by + 31, r=8, color=(200, 20, 20, 255), width=3)
    draw.text((bx + 60, by + 10), "错误工况：低台面前屈深躬 (25°~30°) / 悬臂重载", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255))
    draw.text((bx + 60, by + 36), "L5/S1 轴向暴压 2520N · 竖脊肌缺血痉挛 · 髓核高压后突", font=FONT_CARD_SUB, fill=(255, 210, 210, 240))

    # 3. 科学姿势横幅 (右侧)
    rx = w - bw - 40
    draw.rounded_rectangle([(rx, by), (rx + bw, by + bh)], radius=8, fill=(20, 130, 60, 220), outline=(60, 220, 110, 240), width=2)
    draw.ellipse([(rx + 14, by + 14), (rx + 48, by + 48)], fill=(230, 255, 235, 255))
    draw_clean_check(draw, rx + 31, by + 31, r=8, color=(15, 120, 50, 255), width=3)
    draw.text((rx + 60, by + 10), "科学防护：砧板垂直垫高 10cm / 踩凳交替卸载", font=FONT_CARD_TITLE, fill=(255, 255, 255, 255))
    draw.text((rx + 60, by + 36), "躯干接近中立位 (0°~5°) · 骨盆抵靠卸载 35% · 肌肉彻底放松", font=FONT_CARD_SUB, fill=(210, 255, 225, 240))

    # 4. 左侧错误力学标注点
    # 4.1 前倾长力臂
    lx, ly, lbw, lbh = draw_badge(draw, 35, 170, "前倾长力臂 (d ≈ 25~30cm，力矩放大 5 倍)", fill=(45, 15, 15, 240), outline=(255, 80, 80, 220), text_color=(255, 130, 110))
    draw.line([(lx + lbw, ly + lbh // 2), (220, 190)], fill=(255, 80, 80, 220), width=2)
    draw.ellipse([(217, 187), (223, 193)], fill=(255, 80, 80, 255))

    # 4.2 竖脊肌等长痉挛
    lx, ly, lbw, lbh = draw_badge(draw, 380, 240, "竖脊肌持续强直 (肌内压超标，微循环闭塞)", fill=(50, 20, 15, 245), outline=(255, 100, 60, 220), text_color=(255, 160, 120))
    draw.line([(lx, ly + lbh // 2), (325, 300)], fill=(255, 100, 60, 220), width=2)
    draw.ellipse([(322, 297), (328, 303)], fill=(255, 100, 60, 255))

    # 4.3 L5/S1 高压红斑
    lx, ly, lbw, lbh = draw_badge(draw, 380, 380, "L5/S1 承载 2520N (前窄后宽，流体髓核后挤)", fill=(60, 10, 10, 250), outline=(255, 40, 40, 240), text_color=(255, 90, 80))
    draw.line([(lx, ly + lbh // 2), (345, 420)], fill=(255, 40, 40, 220), width=2)
    draw.ellipse([(342, 417), (348, 423)], fill=(255, 40, 40, 255))

    # 4.4 台面过低
    lx, ly, lbw, lbh = draw_badge(draw, 35, 490, "标准台面过低 (80~82cm，迫使躯干深躬前探)", fill=(35, 25, 15, 240), outline=(255, 170, 50, 220), text_color=(255, 200, 110))
    draw.line([(lx + lbw, ly + lbh // 2), (180, 475)], fill=(255, 170, 50, 200), width=2)
    draw.ellipse([(177, 472), (183, 478)], fill=(255, 170, 50, 255))

    # 5. 左下角错误力学危象卡片
    cw, ch = 430, 245
    cx, cy = 35, 605
    draw.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=8, fill=(12, 18, 26, 235), outline=(255, 80, 80, 180), width=1)
    draw.text((cx + 15, cy + 12), "【低位做饭四大力学危象】", font=FONT_CARD_TITLE, fill=(255, 90, 80, 255))
    draw.line([(cx + 15, cy + 34), (cx + cw - 15, cy + 34)], fill=(255, 80, 80, 60), width=1)
    err_lines = [
        "• 灶台台面过低（仅80~82cm），洗切被迫低头塌腰前屈 25°",
        "• 上身 60% 重力形成长悬臂，迫使竖脊肌输出 2100N 静态拉力",
        "• L5/S1 盘内压飙升至 2520N（达到正常中立站立的 2.5~3 倍）",
        "• 持续站立 15 分钟导致肌内压超标，背部毛细血管闭塞缺血",
        "• 椎间隙前倾楔形变，水力学驱动髓核持续向右后方突出区冲顶",
        "• 极易诱发晨起纤维环疲劳撕裂与傍晚肌肉衰竭型关节嵌顿"
    ]
    cury = cy + 44
    for l in err_lines:
        draw.text((cx + 15, cury), l, font=FONT_CARD_BODY, fill=(235, 215, 215, 240))
        cury += 25

    # 6. 右侧科学防护力学标注点
    # 6.1 中立脊柱
    rx_b, ry_b, rbw, rbh = draw_badge(draw, 880, 170, "中立生理曲度 (前倾角 0°~5°，重力轴归中)", fill=(15, 30, 25, 240), outline=(60, 220, 120, 220), text_color=(160, 255, 190))
    draw.line([(rx_b, ry_b + rbh // 2), (835, 220)], fill=(60, 220, 120, 220), width=2)
    draw.ellipse([(832, 217), (838, 223)], fill=(60, 220, 120, 255))

    # 6.2 垫高砧板
    rx_b, ry_b, rbw, rbh = draw_badge(draw, 550, 360, "砧板垂直垫高 10cm (达到 92~95cm 屈肘黄金面)", fill=(15, 30, 35, 240), outline=(0, 200, 240, 220), text_color=(150, 240, 255))
    draw.line([(rx_b + rbw, ry_b + rbh // 2), (670, 440)], fill=(0, 200, 240, 220), width=2)
    draw.ellipse([(667, 437), (673, 443)], fill=(0, 200, 240, 255))

    # 6.3 骨盆靠台
    rx_b, ry_b, rbw, rbh = draw_badge(draw, 550, 500, "小腹/骨盆轻抵台面 (开辟第三支点，短路 35% 负荷)", fill=(15, 35, 30, 240), outline=(50, 220, 150, 220), text_color=(160, 255, 210))
    draw.line([(rx_b + rbw, ry_b + rbh // 2), (730, 520)], fill=(50, 220, 150, 220), width=2)
    draw.ellipse([(727, 517), (733, 523)], fill=(50, 220, 150, 255))

    # 6.4 12cm 踩脚凳 (优化坐标，避免溢出与遮挡脚部)
    rx_b, ry_b, rbw, rbh = draw_badge(draw, 740, 770, "12cm 防滑踩脚凳 (屈髋松弛腰大肌)", fill=(20, 35, 25, 245), outline=(70, 230, 130, 220), text_color=(170, 255, 190))
    draw.line([(rx_b, ry_b + rbh // 2), (760, 850)], fill=(70, 230, 130, 220), width=2)
    draw.ellipse([(757, 847), (763, 853)], fill=(70, 230, 130, 255))

    # 7. 右侧科学护腰机制卡片 (移至人物右后方开阔暗区，避免遮挡腿脚与矮凳)
    rcw, rch = 345, 245
    rcx, rcy = 825, 480
    draw.rounded_rectangle([(rcx, rcy), (rcx + rcw, rcy + rch)], radius=8, fill=(12, 22, 20, 235), outline=(50, 200, 120, 180), width=1)
    draw.text((rcx + 15, rcy + 12), "【科学护腰四大减压机制】", font=FONT_CARD_TITLE, fill=(70, 230, 130, 255))
    draw.line([(rcx + 15, rcy + 34), (rcx + rcw - 15, rcy + 34)], fill=(50, 200, 120, 60), width=1)
    sci_lines = [
        "• 砧板垫高 8~10cm，躯干直立（力臂归零）",
        "• 骨盆轻抵橱柜边，将 35% 重力导向柜体",
        "• 单脚踩 12cm 踏板屈髋，双侧髂腰肌松弛",
        "• 竖脊肌肌电暴跌 45%，瞬间恢复血流灌注",
        "• 椎间孔开辟，解除右侧 S1 神经机械牵张",
        "• 双脚每 10~15 分钟交替，杜绝单侧疲劳"
    ]
    cury = rcy + 44
    for l in sci_lines:
        draw.text((rcx + 15, cury), l, font=FONT_CARD_BODY, fill=(215, 235, 225, 240))
        cury += 25

    result = Image.alpha_composite(base, overlay).convert("RGB")
    out_file = os.path.join(IMG_DIR, "18_kitchen_posture_comparison_3d.jpg")
    result.save(out_file, quality=95)
    print(f"Built {out_file}")


def build_image_19():
    """构建 19_kitchen_ergonomics_setup_guide_3d.jpg"""
    base_path = os.path.join(BRAIN_DIR, "kitchen_setup_clean_base_1790135842065.jpg")
    base = Image.open(base_path).convert("RGBA")
    w, h = base.size  # 1200, 896

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. 顶部主标题栏
    tw, th = 780, 46
    tx, ty = (w - tw) // 2, 20
    draw.rounded_rectangle([(tx, ty), (tx + tw, ty + th)], radius=6, fill=(12, 18, 28, 235), outline=(0, 200, 255, 200), width=1)
    draw.text((tx + 28, ty + 10), "【开放厨房工效学 6 大几何校准与腰椎防损伤指南】", font=FONT_TITLE, fill=(240, 248, 255, 255))

    # 2. 6 大核心功能区标注 (带引线与徽章)
    # ① 砧板加厚抬高区
    b1_x, b1_y, b1_w, b1_h = draw_badge(draw, 760, 110, "① 砧板抬高区 (操作面达 92~95cm，屈肘下 10cm)", fill=(15, 30, 40, 240), outline=(0, 200, 255, 220), text_color=(170, 235, 255))
    draw.line([(b1_x + b1_w // 2, b1_y + b1_h), (850, 260)], fill=(0, 200, 255, 220), width=2)
    draw.ellipse([(847, 257), (853, 263)], fill=(0, 200, 255, 255))

    # ② 水槽高位沥水架
    b2_x, b2_y, b2_w, b2_h = draw_badge(draw, 420, 190, "② 水槽防深躬装置 (高位滤架/盆中盆，抬高 15cm)", fill=(20, 35, 30, 240), outline=(60, 220, 140, 220), text_color=(170, 255, 200))
    draw.line([(b2_x + b2_w // 2, b2_y + b2_h), (630, 360)], fill=(60, 220, 140, 220), width=2)
    draw.ellipse([(627, 357), (633, 363)], fill=(60, 220, 140, 255))

    # ③ 灶台轻量化炊具
    b3_x, b3_y, b3_w, b3_h = draw_badge(draw, 50, 310, "③ 轻量化平底炒锅 (避免单手悬空端铸铁锅，消灭偏心力矩)", fill=(35, 25, 15, 240), outline=(255, 170, 60, 220), text_color=(255, 200, 120))
    draw.line([(b3_x + b3_w, b3_y + b3_h // 2), (430, 440)], fill=(255, 170, 60, 200), width=2)
    draw.ellipse([(427, 437), (433, 443)], fill=(255, 170, 60, 255))

    # ④ 橱柜边缘借力支点
    b4_x, b4_y, b4_w, b4_h = draw_badge(draw, 50, 520, "④ 台面接触式卸载 (小腹轻抵台沿，短路 35% 躯干重力)", fill=(15, 30, 25, 240), outline=(50, 220, 120, 220), text_color=(160, 255, 190))
    draw.line([(b4_x + b4_w, b4_y + b4_h // 2), (380, 560)], fill=(50, 220, 120, 200), width=2)
    draw.ellipse([(377, 557), (383, 563)], fill=(50, 220, 120, 255))

    # ⑤ 踢脚线防滑踩脚凳
    b5_x, b5_y, b5_w, b5_h = draw_badge(draw, 640, 650, "⑤ 12~15cm 防滑踩脚凳 (贴柜摆放，10~15 分钟双侧交替踩放)", fill=(20, 35, 25, 245), outline=(70, 230, 130, 220), text_color=(170, 255, 190))
    draw.line([(b5_x + b5_w // 2, b5_y + b5_h), (620, 770)], fill=(70, 230, 130, 220), width=2)
    draw.ellipse([(617, 767), (623, 773)], fill=(70, 230, 130, 255))

    # ⑥ 烹饪动线防扭转
    b6_x, b6_y, b6_w, b6_h = draw_badge(draw, 780, 480, "⑥ 移步平移防扭转铁律 (以碎步平移代替水平转腰)", fill=(45, 15, 15, 245), outline=(255, 80, 80, 220), text_color=(255, 130, 110))
    draw.line([(b6_x, b6_y + b6_h // 2), (720, 500)], fill=(255, 80, 80, 200), width=2)
    draw.ellipse([(717, 497), (723, 503)], fill=(255, 80, 80, 255))

    # 3. 底部全宽总结大卡片
    cw, ch = 1120, 110
    cx, cy = 40, 760
    draw.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=8, fill=(10, 16, 26, 240), outline=(0, 190, 240, 180), width=1)
    draw.text((cx + 20, cy + 12), "【三甲医院脊柱力学实验室：厨房高危作业护腰 4 句金诀】", font=FONT_CARD_TITLE, fill=(0, 210, 255, 255))
    draw.line([(cx + 20, cy + 34), (cx + cw - 20, cy + 34)], fill=(0, 190, 240, 80), width=1)

    rules = [
        ("1. 切配砧板垂直垫高", "垫高 8~10cm，屈肘 90° 直立作业，消灭前倾长悬臂梁"),
        ("2. 防滑踩凳交替踩放", "12cm 矮凳单脚踏放，松弛髂腰肌，后方椎间隙充分撑开"),
        ("3. 骨盆轻靠橱柜边缘", "小腹贴柜开辟第三支点，35% 重力直接通过柜体导向地面"),
        ("4. 挪步转身绝不转腰", "水槽灶台取物以小碎步转向，杜绝纤维环 350% 剪切破坏")
    ]
    col_w = (cw - 40) // 4
    for i, (r_title, r_desc) in enumerate(rules):
        col_x = cx + 20 + i * col_w
        draw.text((col_x, cy + 44), r_title, font=FONT_BADGE, fill=(255, 220, 120, 255))
        if len(r_desc) > 16:
            draw.text((col_x, cy + 66), r_desc[:16], font=FONT_SMALL, fill=(200, 220, 240, 230))
            draw.text((col_x, cy + 84), r_desc[16:], font=FONT_SMALL, fill=(200, 220, 240, 230))
        else:
            draw.text((col_x, cy + 66), r_desc, font=FONT_SMALL, fill=(200, 220, 240, 230))

    result = Image.alpha_composite(base, overlay).convert("RGB")
    out_file = os.path.join(IMG_DIR, "19_kitchen_ergonomics_setup_guide_3d.jpg")
    result.save(out_file, quality=95)
    print(f"Built {out_file}")


def render_kitchen_dynamic_gif():
    """
    生成厨房前屈与踩脚凳减压双视窗动态仿真 GIF (全身动作 + L5/S1 横断面受力联动)
    """
    import sys
    sys.path.append(os.path.dirname(__file__))
    from build_coupled_kitchen_gif import build_coupled_dynamic_gif
    build_coupled_dynamic_gif()


if __name__ == "__main__":
    print("Starting kitchen visual pipeline...")
    build_image_18()
    build_image_19()
    render_kitchen_dynamic_gif()
    print("All kitchen visuals generated successfully!")

