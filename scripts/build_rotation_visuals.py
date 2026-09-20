#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProtectingLumbarSpine - 水平转腰与侧卧斜扳力学毁灭机制 3D 图解与动态 GIF 生成脚本
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
FONT_BADGE = ImageFont.truetype(FONT_BOLD_PATH, 13)
FONT_TELEMETRY = ImageFont.truetype(FONT_PATH, 12)
FONT_ALERT = ImageFont.truetype(FONT_PATH, 12)

BRAIN_DIR = r"C:\Users\Administrator\.gemini\antigravity-ide\brain\6e0c6eac-6e3a-4675-b0d6-b33b30b16601"
IMG_DIR = "media/images"
VIDEO_DIR = "media/video"
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def draw_badge(draw, x, y, text, fill=(15, 22, 32, 235), outline=(0, 180, 240, 200), text_color=(240, 245, 255)):
    bbox = FONT_BADGE.getbbox(text)
    bw, bh = bbox[2] - bbox[0] + 16, bbox[3] - bbox[1] + 12
    draw.rounded_rectangle([(x, y), (x + bw, y + bh)], radius=4, fill=fill, outline=outline, width=1)
    draw.text((x + 8, y + 4), text, font=FONT_BADGE, fill=text_color)
    return (x, y, bw, bh)


def build_image_16():
    """构建 16_lumbar_rotation_biomechanics_3d.jpg"""
    base_path = os.path.join(BRAIN_DIR, "lumbar_rotation_clean_base_1789892975529.jpg")
    base = Image.open(base_path).convert("RGBA")
    w, h = base.size  # 1200, 896

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 顶部标题栏
    tw, th = 680, 46
    tx, ty = (w - tw) // 2, 25
    draw.rounded_rectangle([(tx, ty), (tx + tw, ty + th)], radius=6, fill=(12, 18, 28, 230), outline=(255, 80, 80, 220), width=1)
    draw.text((tx + 24, ty + 10), "【腰椎生理旋转限制与侧卧斜扳力学毁灭机制】", font=FONT_TITLE, fill=(255, 220, 220, 255))

    # 1. 矢状面小关节限制
    bx, by, bw, bh = draw_badge(draw, 180, 160, "矢状面小关节 (单节生理旋转仅 1°~1.5°)", fill=(15, 25, 35, 240), outline=(0, 200, 255, 220), text_color=(180, 230, 255))
    draw.line([(bx + bw // 2, by + bh), (380, 360)], fill=(0, 200, 255, 200), width=2)
    draw.ellipse([(377, 357), (383, 363)], fill=(0, 200, 255, 255))

    # 2. 拧毛巾剪切破坏
    bx, by, bw, bh = draw_badge(draw, 640, 150, "扭转剪切力 (拧毛巾效应 · 50% 纤维环失效)", fill=(45, 15, 15, 245), outline=(255, 80, 80, 220), text_color=(255, 120, 100))
    draw.line([(bx + bw // 2, by + bh), (570, 480)], fill=(255, 80, 80, 220), width=2)
    draw.ellipse([(567, 477), (573, 483)], fill=(255, 80, 80, 255))

    # 3. 骨盆长力臂杠杆
    bx, by, bw, bh = draw_badge(draw, 720, 680, "骨盆长杠杆 (斜扳法施加数倍破坏性扭矩)", fill=(35, 25, 10, 245), outline=(255, 170, 50, 220), text_color=(255, 200, 100))
    draw.line([(bx, by + bh // 2), (640, 620)], fill=(255, 170, 50, 200), width=2)
    draw.ellipse([(637, 617), (643, 623)], fill=(255, 170, 50, 255))

    # 4. 左下角科学剖析卡片
    cw, ch = 380, 150
    cx, cy = 40, 700
    draw.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=8, fill=(12, 18, 26, 230), outline=(255, 80, 80, 180), width=1)
    draw.text((cx + 15, cy + 12), "【为什么侧卧转腰/斜扳会剧痛？】", font=FONT_CARD_TITLE, fill=(255, 90, 80, 255))
    draw.line([(cx + 15, cy + 34), (cx + cw - 15, cy + 34)], fill=(255, 80, 80, 60), width=1)
    lines = [
        "• 腰椎关节面呈矢状垂直分布，天生禁止水平旋转",
        "• 旋转超过 2° 即触发小关节面硬碰硬暴力咬合",
        "• 纤维环呈交错排列，扭转时半数纤维完全松弛罢工",
        "• 剩余纤维承受 300% 极限剪切撕裂，髓核被迫向后爆突"
    ]
    cury = cy + 42
    for l in lines:
        draw.text((cx + 15, cury), l, font=FONT_CARD_BODY, fill=(230, 215, 215, 240))
        cury += 24

    result = Image.alpha_composite(base, overlay).convert("RGB")
    out_file = os.path.join(IMG_DIR, "16_lumbar_rotation_biomechanics_3d.jpg")
    result.save(out_file, quality=95)
    print(f"Built {out_file}")


def build_image_17():
    """构建 17_l5s1_axial_rotation_nerve_shear_3d.jpg"""
    base_path = os.path.join(BRAIN_DIR, "l5s1_axial_clean_rotation_1789892944925.jpg")
    base = Image.open(base_path).convert("RGBA")
    w, h = base.size

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. 小关节撞击
    draw_badge(draw, 740, 140, "小关节撞击咬合 (骨性阻挡破坏)", fill=(50, 15, 15, 245), outline=(255, 80, 80, 220), text_color=(255, 120, 100))
    draw.line([(740, 155), (660, 270)], fill=(255, 80, 80, 220), width=2)
    draw.ellipse([(657, 267), (663, 273)], fill=(255, 80, 80, 255))

    # 2. 纤维环剪切撕裂
    draw_badge(draw, 640, 680, "纤维环扭转剪切撕裂 (拧毛巾效应)", fill=(50, 15, 15, 245), outline=(255, 90, 70, 220), text_color=(255, 130, 90))
    draw.line([(640, 695), (550, 650)], fill=(255, 90, 70, 200), width=2)
    draw.ellipse([(547, 647), (553, 653)], fill=(255, 90, 70, 255))

    # 3. 神经根剪切绞杀
    draw_badge(draw, 780, 360, "右侧 S1 神经根 (剪切碾磨型极度剧痛)", fill=(55, 10, 10, 250), outline=(255, 50, 50, 240), text_color=(255, 100, 80))
    draw.line([(780, 375), (710, 420)], fill=(255, 50, 50, 220), width=2)
    draw.ellipse([(707, 417), (713, 423)], fill=(255, 50, 50, 255))

    # 4. 突出物横向挤压
    draw_badge(draw, 340, 320, "髓核流体受扭挤压暴突", fill=(15, 25, 35, 240), outline=(0, 180, 240, 200), text_color=(180, 220, 255))
    draw.line([(450, 340), (560, 480)], fill=(0, 180, 240, 200), width=2)
    draw.ellipse([(557, 477), (563, 483)], fill=(0, 180, 240, 255))

    # 5. 左侧神经受牵
    draw_badge(draw, 40, 420, "左侧 S1 神经根 (被动受牵张)")
    draw.line([(240, 435), (320, 445)], fill=(0, 180, 240, 200), width=2)
    draw.ellipse([(317, 442), (323, 448)], fill=(0, 180, 240, 255))

    result = Image.alpha_composite(base, overlay).convert("RGB")
    out_file = os.path.join(IMG_DIR, "17_l5s1_axial_rotation_nerve_shear_3d.jpg")
    result.save(out_file, quality=95)
    print(f"Built {out_file}")


def render_rotation_gif():
    """生成轴位转腰剪切动态演进 GIF: axial_rotation_nerve_crush.gif"""
    base_path = os.path.join(BRAIN_DIR, "l5s1_axial_clean_rotation_1789892944925.jpg")
    base_img = Image.open(base_path).convert("RGBA")

    target_w, target_h = 800, 600
    img_area_h = 475
    scaled_base = base_img.resize((target_w, int(base_img.height * target_w / base_img.width)), Image.Resampling.LANCZOS)
    top_crop = max(0, (scaled_base.height - img_area_h) // 2)
    cropped_base = scaled_base.crop((0, top_crop, target_w, top_crop + img_area_h))

    prot_cx, prot_cy = 440, 250
    nerve_cx, nerve_cy = 500, 230
    facet_cx, facet_cy = 470, 140

    total_frames = 60
    frames = []

    for i in range(total_frames):
        frame = Image.new("RGBA", (target_w, target_h), (10, 14, 20, 255))

        # 阶段划分：
        # 0 ~ 12: 中立位 (0° 旋转)
        # 13 ~ 26: 进入旋转 (0° ➔ 1.5° 生理极限)
        # 27 ~ 47: 强制斜扳 / 暴力转腰 (1.5° ➔ 3.8° 严重超限，小关节撞击 + 剪切暴突)
        # 48 ~ 59: 复位卸载
        if i <= 12:
            phase_desc = "状态：中立未旋转 (腰椎保持中立平衡，小关节间隙平整)"
            rot_deg = "0.0° (中立)"
            facet_stress = "0 N (间隙通畅)"
            facet_color = (80, 230, 120, 255)
            shear_stress = "0% (无剪切)"
            shear_color = (80, 230, 120, 255)
            prot_depth = "5.6 mm (基线)"
            prot_color = (255, 210, 100, 255)
            nerve_status = "血流通畅 (无剪切)"
            nerve_color = (80, 230, 120, 255)
            is_shear_crush = False
            prog = 0.0
        elif i <= 26:
            p = (i - 12) / 14.0
            prog = p * 0.4
            phase_desc = f"状态：身体微转腰 (旋转 {p*1.5:.1f}°，逼近生理临界止动点)"
            rot_deg = f"{p*1.5:.1f}° (生理极限)"
            facet_stress = f"{int(250*p)} N (接触初现)"
            facet_color = (255, 180, 70, 255)
            shear_stress = f"{int(120*p)}% (开始扭曲)"
            shear_color = (255, 180, 70, 255)
            d = round(5.6 + 0.3 * p, 1)
            prot_depth = f"{d} mm (向外侧偏推)"
            prot_color = (255, 160, 80, 255)
            nerve_status = "轻微接触摩擦"
            nerve_color = (255, 180, 70, 255)
            is_shear_crush = False
        elif i <= 47:
            p = (i - 26) / 21.0
            prog = 1.0
            pulse = math.sin(p * math.pi * 4) * 0.08
            cur_d = round(6.5 + pulse, 1)
            cur_deg = round(3.5 + math.sin(p * math.pi * 4) * 0.2, 1)
            cur_fx = int(850 + math.sin(p * math.pi * 4) * 50)
            phase_desc = "动作：侧卧推拿斜扳 / 暴力转腰 (小关节硬撞击，纤维环拧毛巾剪切撕裂!)"
            rot_deg = f"{cur_deg}° (超出生理230%)"
            facet_stress = f"{cur_fx} N (硬碰硬撞击)"
            facet_color = (255, 50, 50, 255)
            shear_stress = "360% (50%纤维失效)"
            shear_color = (255, 50, 50, 255)
            prot_depth = f"{cur_d} mm (剪切挤出)"
            prot_color = (255, 50, 50, 255)
            nerve_status = "剪切碾磨 (爆发性剧痛)"
            nerve_color = (255, 50, 50, 255)
            is_shear_crush = True
        else:
            p = (i - 47) / 12.0
            prog = 1.0 - p
            phase_desc = "动作：松开外力卸载回弹 (遗留急性水肿与小关节挫伤)"
            cur_deg = round(3.5 * (1 - p), 1)
            rot_deg = f"{cur_deg}° (回弹中)"
            facet_stress = f"{int(850*(1-p))} N"
            facet_color = (255, 160, 90, 255)
            shear_stress = f"{int(360*(1-p))}%"
            shear_color = (255, 180, 90, 255)
            d = round(5.8 - 0.2 * p, 1)
            prot_depth = f"{d} mm"
            prot_color = (255, 160, 90, 255)
            nerve_status = "反应性水肿高敏"
            nerve_color = (255, 120, 80, 255)
            is_shear_crush = (p < 0.25)

        current_slice = cropped_base.copy()
        overlay = Image.new("RGBA", current_slice.size, (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        if is_shear_crush:
            # 1. 小关节骨质撞击火花
            draw_ov.ellipse([(facet_cx - 15, facet_cy - 15), (facet_cx + 15, facet_cy + 15)], fill=(255, 60, 60, 160))
            # 2. 神经根剪切碾磨电火花波纹
            for ang in range(0, 360, 30):
                theta = math.radians(ang + (i * 25) % 360)
                px1 = nerve_cx + math.cos(theta) * 12
                py1 = nerve_cy + math.sin(theta) * 12
                px2 = nerve_cx + math.cos(theta) * 28
                py2 = nerve_cy + math.sin(theta) * 28
                draw_ov.line([(px1, py1), (px2, py2)], fill=(255, 240, 60, 240), width=2)
            # 3. 纤维环螺旋剪切线
            shear_ring = int(35 + (i % 6) * 5)
            draw_ov.ellipse(
                [(prot_cx - shear_ring, prot_cy - shear_ring), (prot_cx + shear_ring, prot_cy + shear_ring)],
                outline=(255, 70, 70, 210), width=2
            )
        elif prog > 0.1:
            draw_ov.ellipse(
                [(prot_cx - 20, prot_cy - 20), (prot_cx + 20, prot_cy + 20)],
                fill=(240, 60, 60, int(80 * prog))
            )

        current_slice = Image.alpha_composite(current_slice, overlay)
        frame.paste(current_slice, (0, 62))

        # HUD 悬浮面板
        draw_hud = ImageDraw.Draw(frame)
        card_x, card_y = 20, 78
        card_w, card_h = 245, 130
        hud_lines = [
            ("椎体扭转角:", rot_deg, (255, 220, 100, 255)),
            ("小关节撞击力:", facet_stress, facet_color),
            ("纤维环剪切力:", shear_stress, shear_color),
            ("突入椎管深度:", prot_depth, prot_color),
            ("S1神经根状态:", nerve_status, nerve_color),
        ]
        # 玻璃卡片
        draw_hud.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=6, fill=(10, 16, 26, 215), outline=(255, 80, 80, 180) if is_shear_crush else (0, 180, 240, 180), width=1)
        draw_hud.line([(card_x + 8, card_y + 26), (card_x + card_w - 8, card_y + 26)], fill=(255, 80, 80, 80) if is_shear_crush else (0, 180, 240, 80), width=1)
        draw_hud.text((card_x + 10, card_y + 6), "【L5/S1 扭转剪切遥测】", font=FONT_CARD_TITLE, fill=(255, 90, 80, 255) if is_shear_crush else (0, 200, 255, 255))
        cy_text = card_y + 32
        for label, val, val_color in hud_lines:
            draw_hud.text((card_x + 10, cy_text), label, font=FONT_CARD_BODY, fill=(180, 200, 220, 240))
            draw_hud.text((card_x + 115, cy_text), val, font=FONT_CARD_BODY, fill=val_color)
            cy_text += 20

        # 顶部标题栏
        draw_hud.rectangle([(0, 0), (target_w, 62)], fill=(12, 18, 26, 255))
        draw_hud.line([(0, 61), (target_w, 61)], fill=(35, 48, 68, 255), width=1)
        draw_hud.text((18, 8), "【L5/S1 横断面微观力学演变】水平转腰与斜扳：小关节撞击与神经剪切碾磨", font=FONT_TITLE, fill=(240, 245, 255))
        sub_color = (255, 80, 80) if is_shear_crush else (150, 185, 225)
        draw_hud.text((18, 35), phase_desc, font=FONT_CARD_BODY, fill=sub_color)

        # 底部状态栏
        draw_hud.rectangle([(0, 537), (target_w, 600)], fill=(12, 18, 26, 255))
        draw_hud.line([(0, 537), (target_w, 537)], fill=(35, 48, 68, 255), width=1)

        line1_text = "解剖铁律: 腰椎小关节呈矢状位天生禁转 | 拧毛巾效应: 半数纤维环完全松弛失效，剪切力暴增300%"
        draw_hud.text((18, 544), line1_text, font=FONT_TELEMETRY, fill=(180, 205, 230))

        if is_shear_crush:
            # 黄色警示三角
            draw_hud.polygon([(18 + 7, 570), (18 + 14, 570 + 14), (18, 570 + 14)], fill=(255, 204, 0))
            draw_hud.line([(18 + 7, 573), (18 + 7, 578)], fill=(0, 0, 0), width=2)
            draw_hud.ellipse([(18 + 6, 580), (18 + 8, 582)], fill=(0, 0, 0))
            alert_text = "致命禁忌警报: 严禁腰突患者盲目旋转推拿或侧卧斜扳！高危剪切力极易诱发纤维环终末断裂与髓核急性脱出!"
            draw_hud.text((38, 569), alert_text, font=FONT_ALERT, fill=(255, 80, 80))
        else:
            draw_hud.text((18, 569), "力学机理: 侧趴斜扳利用骨盆与肩部形成超长力臂，施加破坏性杠杆扭矩，强行突破 1.5° 生理骨性极限。", font=FONT_ALERT, fill=(120, 165, 210))

        frames.append(frame.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG))

    out_path = os.path.join(VIDEO_DIR, "axial_rotation_nerve_crush.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=40, loop=0)
    print(f"Generated {out_path}, size: {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    print("正在构建水平转腰与斜扳机制 100% 纯中文 3D 图谱...")
    build_image_16()
    build_image_17()
    print("正在渲染转腰对神经根剪切碾磨动态 GIF 动图...")
    render_rotation_gif()
    print("全部转腰力学可视化资产构建完成！")
