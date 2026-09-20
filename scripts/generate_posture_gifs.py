#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProtectingLumbarSpine - 轴位横断面高保真医学动图渲染器 (V2 极致精修版)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FONT_TITLE = ImageFont.truetype(FONT_PATH, 18)
FONT_SUB = ImageFont.truetype(FONT_PATH, 13)
FONT_HUD_HEAD = ImageFont.truetype(FONT_PATH, 13)
FONT_HUD_BODY = ImageFont.truetype(FONT_PATH, 12)
FONT_BOTTOM_LINE1 = ImageFont.truetype(FONT_PATH, 12)
FONT_BOTTOM_LINE2 = ImageFont.truetype(FONT_PATH, 12)

OUTPUT_DIR = "media/video"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_warning_badge(draw, x, y, size=14):
    """绘制高清晰度警示黄色三角与惊叹号"""
    half = size / 2.0
    pts = [(x + half, y), (x + size, y + size), (x, y + size)]
    draw.polygon(pts, fill=(255, 204, 0))
    draw.line([(x + half, y + 3), (x + half, y + 8)], fill=(0, 0, 0), width=2)
    draw.ellipse([(x + half - 1, y + 10), (x + half + 1, y + 12)], fill=(0, 0, 0))


def draw_glass_card(draw, x, y, w, h, title, lines, border_color=(0, 200, 255, 160)):
    """绘制高科技半透明玻璃质感遥测卡片"""
    # 背景
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=6, fill=(10, 16, 26, 210), outline=border_color, width=1)
    # 标题栏底线
    draw.line([(x + 8, y + 26), (x + w - 8, y + 26)], fill=(border_color[0], border_color[1], border_color[2], 80), width=1)
    # 标题文本
    draw.text((x + 10, y + 6), title, font=FONT_HUD_HEAD, fill=(border_color[0], border_color[1], border_color[2], 255))
    # 逐行内容
    cur_y = y + 32
    for label, val, val_color in lines:
        draw.text((x + 10, cur_y), label, font=FONT_HUD_BODY, fill=(180, 200, 220, 240))
        # 右对齐或紧随其后
        draw.text((x + 115, cur_y), val, font=FONT_HUD_BODY, fill=val_color)
        cur_y += 20


def draw_corner_brackets(draw, cx, cy, sz, color=(255, 200, 50, 200), width=2):
    """绘制目标锁定方框四个角标"""
    d = sz // 2
    l = sz // 4
    # 左上
    draw.line([(cx - d, cy - d), (cx - d + l, cy - d)], fill=color, width=width)
    draw.line([(cx - d, cy - d), (cx - d, cy - d + l)], fill=color, width=width)
    # 右上
    draw.line([(cx + d, cy - d), (cx + d - l, cy - d)], fill=color, width=width)
    draw.line([(cx + d, cy - d), (cx + d, cy - d + l)], fill=color, width=width)
    # 左下
    draw.line([(cx - d, cy + d), (cx - d + l, cy + d)], fill=color, width=width)
    draw.line([(cx - d, cy + d), (cx - d, cy + d - l)], fill=color, width=width)
    # 右下
    draw.line([(cx + d, cy + d), (cx + d - l, cy + d)], fill=color, width=width)
    draw.line([(cx + d, cy + d), (cx + d, cy + d - l)], fill=color, width=width)


def render_geyou_gif():
    base_img_path = "media/images/11_l5s1_geyou_slump_axial_3d.jpg"
    base_img = Image.open(base_img_path).convert("RGBA")
    
    target_w, target_h = 800, 600
    img_area_h = 475
    scaled_base = base_img.resize((target_w, int(base_img.height * target_w / base_img.width)), Image.Resampling.LANCZOS)
    top_crop = max(0, (scaled_base.height - img_area_h) // 2)
    cropped_base = scaled_base.crop((0, top_crop, target_w, top_crop + img_area_h))

    # 关键解剖坐标（图像区域内）
    prot_cx, prot_cy = 310, 245
    nerve_cx, nerve_cy = 220, 220

    total_frames = 60
    frames = []

    for i in range(total_frames):
        # 1. 底层画布
        frame = Image.new("RGBA", (target_w, target_h), (10, 14, 20, 255))
        
        # 2. 状态阶段划分
        # 0 ~ 12: 中立端坐
        # 13 ~ 28: 滑入葛优躺 (骨盆后倾，腰椎悬空屈曲)
        # 29 ~ 47: 45分钟瘫坐蠕变压迫峰值
        # 48 ~ 59: 起身恢复过渡
        if i <= 12:
            phase = "中立端坐"
            phase_desc = "姿态：健康端正坐姿 (腰椎保持 30° 生理前凸，竖脊肌正常激活维持力学平衡)"
            prog = 0.0
            pelvis_deg = "0° (中立)"
            posture_state = "生理前凸 30°"
            frp_status = "竖脊肌主动收缩 (平衡)"
            frp_color = (80, 230, 120, 255)
            tension_val = "100% (生理负荷)"
            tension_color = (180, 210, 230, 255)
            depth_val = "5.6 mm (基线)"
            depth_color = (255, 210, 100, 255)
            nerve_status = "通畅充盈 (100% 灌注)"
            nerve_color = (80, 230, 120, 255)
            is_alert = False
        elif i <= 28:
            phase = "滑入葛优躺"
            p = (i - 12) / 16.0
            prog = p
            phase_desc = f"姿态：滑入葛优躺瘫坐 (骨盆后倾 {-int(35*p)}°，腰椎悬空，竖脊肌反射性关机)"
            pelvis_deg = f"-{int(35*p)}° (后倾)"
            posture_state = f"屈曲 {int(75*p)}% (腰部悬空)"
            frp_status = f"FRP静默中 ({int(100*p)}% 停工)"
            frp_color = (255, 180, 60, 255)
            tension_val = f"{int(100 + 150*p)}% (拉伸)"
            tension_color = (255, 150, 80, 255)
            d = round(5.6 + 0.3 * p, 1)
            depth_val = f"{d} mm (受挤后移)"
            depth_color = (255, 120, 80, 255)
            nerve_status = f"{int(100 - 65*p)}% 阻力上升"
            nerve_color = (255, 180, 60, 255)
            is_alert = False
        elif i <= 47:
            phase = "长时瘫坐蠕变峰值"
            p = (i - 28) / 19.0
            prog = 1.0
            pulse = math.sin(p * math.pi * 2) * 0.04
            cur_d = round(6.2 + pulse, 1)
            phase_desc = "姿态：葛优躺瘫坐达45分钟 (腰椎完全悬空，后方纤维环极限蠕变，神经持续缺血)"
            pelvis_deg = "-35° (极限后倾)"
            posture_state = "完全后凸 (悬空梁)"
            frp_status = "FRP彻底静默 (0% 肌力)"
            frp_color = (255, 80, 80, 255)
            tension_val = "280% (塑性蠕变)"
            tension_color = (255, 70, 70, 255)
            depth_val = f"{cur_d} mm (峰值外突)"
            depth_color = (255, 60, 60, 255)
            nerve_status = "0% 微循环闭塞缺血"
            nerve_color = (255, 60, 60, 255)
            is_alert = True
        else:
            phase = "起身恢复"
            p = (i - 47) / 12.0
            prog = 1.0 - p
            phase_desc = "姿态：准备发力起身调整 (受压神经根缺血再灌注，肌群重新激活)"
            pelvis_deg = f"-{int(35*(1-p))}°"
            posture_state = f"前凸恢复中 ({int(100*p)}%)"
            frp_status = "竖脊肌反射性微弱收缩"
            frp_color = (255, 200, 100, 255)
            tension_val = f"{int(100 + 180*(1-p))}%"
            tension_color = (255, 160, 90, 255)
            d = round(5.6 + 0.6 * (1 - p), 1)
            depth_val = f"{d} mm"
            depth_color = (255, 140, 90, 255)
            nerve_status = f"{int(70*p)}% 反应性充血"
            nerve_color = (255, 200, 80, 255)
            is_alert = (p < 0.4)

        # 3. 图像层与特效合成
        current_slice = cropped_base.copy()
        
        # 创建半透明特效叠加层
        overlay = Image.new("RGBA", current_slice.size, (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # A. 髓核后移与突出区域高亮脉动光晕
        if prog > 0.05:
            # 突出物中心热应力光晕
            glow_r = int(35 + prog * 30)
            glow_alpha = int(110 * prog)
            for r in range(glow_r, 12, -4):
                alpha = int(glow_alpha * (1.0 - (r - 12) / (glow_r - 12)) ** 1.5)
                draw_ov.ellipse(
                    [(prot_cx - r, prot_cy - r), (prot_cx + r, prot_cy + r)],
                    fill=(240, 50, 40, alpha)
                )

        # B. 神经根压迫靶标与电脉冲
        if is_alert:
            # 旋转扫描脉冲环
            pulse_ring = int(22 + (i % 6) * 4)
            draw_ov.ellipse(
                [(nerve_cx - pulse_ring, nerve_cy - pulse_ring), (nerve_cx + pulse_ring, nerve_cy + pulse_ring)],
                outline=(255, 220, 60, 210), width=2
            )
            draw_corner_brackets(draw_ov, nerve_cx, nerve_cy, sz=38, color=(255, 230, 70, 240), width=2)
            # 痛觉放电波
            for ang in range(0, 360, 60):
                theta = math.radians(ang + (i * 12) % 360)
                px1 = nerve_cx + math.cos(theta) * 12
                py1 = nerve_cy + math.sin(theta) * 12
                px2 = nerve_cx + math.cos(theta) * 26
                py2 = nerve_cy + math.sin(theta) * 26
                draw_ov.line([(px1, py1), (px2, py2)], fill=(255, 240, 80, 220), width=2)

        # 合成叠加层到图像
        current_slice = Image.alpha_composite(current_slice, overlay)

        # C. 贴入总画布中央 (y=62)
        frame.paste(current_slice, (0, 62))

        # D. 绘制左上角科技 HUD 悬浮遥测卡片 (在图像之上)
        draw_hud = ImageDraw.Draw(frame)
        card_x, card_y = 20, 78
        card_w, card_h = 240, 130
        hud_lines = [
            ("骨盆后倾角:", pelvis_deg, (220, 235, 255, 255)),
            ("竖脊肌肌电:", frp_status, frp_color),
            ("后纤维环张力:", tension_val, tension_color),
            ("突入椎管深度:", depth_val, depth_color),
            ("S1神经血流:", nerve_status, nerve_color),
        ]
        draw_glass_card(draw_hud, card_x, card_y, card_w, card_h, "【L5/S1 生物力学动态遥测】", hud_lines, border_color=(0, 180, 240, 180))

        # E. 顶部标题栏 (y: 0 ~ 62)
        draw_hud.rectangle([(0, 0), (target_w, 62)], fill=(12, 18, 26, 255))
        draw_hud.line([(0, 61), (target_w, 61)], fill=(35, 48, 68, 255), width=1)
        draw_hud.text((18, 8), "【L5/S1 横断面微观力学演变】葛优躺瘫坐：流体髓核后移与持续牵张缺血", font=FONT_TITLE, fill=(240, 245, 255))
        sub_color = (255, 110, 90) if is_alert else (150, 185, 225)
        draw_hud.text((18, 35), phase_desc, font=FONT_SUB, fill=sub_color)

        # F. 底部状态栏 (y: 537 ~ 600)
        draw_hud.rectangle([(0, 537), (target_w, 600)], fill=(12, 18, 26, 255))
        draw_hud.line([(0, 537), (target_w, 537)], fill=(35, 48, 68, 255), width=1)

        # 第一行全局指标
        line1_text = f"腰椎负荷模型: 悬空两端简支梁 | 屈曲松弛 (FRP): 竖脊肌静默 | 后纤维环: 承受 280% 持续牵张拉应力"
        draw_hud.text((18, 544), line1_text, font=FONT_BOTTOM_LINE1, fill=(180, 205, 230))

        # 第二行临床病理结论
        if is_alert:
            draw_warning_badge(draw_hud, 18, 570, size=15)
            alert_text = "病理警报: S1神经根微血管完全闭塞缺血，组织液水肿渗出，起立瞬间极易突发急性绞锁刺痛!"
            draw_hud.text((38, 569), alert_text, font=FONT_BOTTOM_LINE2, fill=(255, 80, 80))
        else:
            draw_hud.text((18, 569), "力学机理: 腰部悬空使重力转化为屈曲弯矩，流体髓核向压力最低的后外侧裂隙持续渗透迁移。", font=FONT_BOTTOM_LINE2, fill=(120, 165, 210))

        # 转换为带抖动的高品质 GIF 帧
        frames.append(frame.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG))

    out_path = os.path.join(OUTPUT_DIR, "axial_geyou_slump_dynamic.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=40, loop=0)
    print(f"Generated {out_path}, size: {os.path.getsize(out_path)} bytes")


def render_squat_gif():
    base_img_path = "media/images/13_l5s1_squat_valsalva_axial_3d.jpg"
    base_img = Image.open(base_img_path).convert("RGBA")
    
    target_w, target_h = 800, 600
    img_area_h = 475
    scaled_base = base_img.resize((target_w, int(base_img.height * target_w / base_img.width)), Image.Resampling.LANCZOS)
    top_crop = max(0, (scaled_base.height - img_area_h) // 2)
    cropped_base = scaled_base.crop((0, top_crop, target_w, top_crop + img_area_h))

    prot_cx, prot_cy = 310, 245
    nerve_cx, nerve_cy = 220, 220

    total_frames = 60
    frames = []

    for i in range(total_frames):
        frame = Image.new("RGBA", (target_w, target_h), (10, 14, 20, 255))

        # 阶段划分：
        # 0 ~ 12: 立位准备 (中立)
        # 13 ~ 26: 屈髋屈膝深度全蹲
        # 27 ~ 47: Valsalva 屏气用力 (腹压暴增 + 3200N 水锤暴击)
        # 48 ~ 59: 呼气卸载与复位
        if i <= 12:
            phase_desc = "动作：立位站立准备 (轴向载荷 500N，腹内压 15 mmHg，硬膜外静脉平稳)"
            prog = 0.0
            axial_val = "500 N (基线)"
            axial_color = (180, 210, 230, 255)
            iap_val = "15 mmHg (常压)"
            iap_color = (80, 230, 120, 255)
            prot_val = "5.6 mm (基线)"
            prot_color = (255, 210, 100, 255)
            vein_val = "血流通畅无怒张"
            vein_color = (80, 230, 120, 255)
            nerve_val = "0% (生理状态)"
            nerve_color = (80, 230, 120, 255)
            is_burst = False
        elif i <= 26:
            p = (i - 12) / 14.0
            prog = p * 0.5
            phase_desc = f"动作：屈髋屈膝全蹲 (髋屈 {int(120*p)}°，骨盆极限后倾，前缘咬合，轴向压力翻倍)"
            axial_val = f"{int(500 + 900*p)} N (上升)"
            axial_color = (255, 180, 70, 255)
            iap_val = f"{int(15 + 25*p)} mmHg"
            iap_color = (255, 210, 80, 255)
            d = round(5.6 + 0.3 * p, 1)
            prot_val = f"{d} mm (前压后顶)"
            prot_color = (255, 140, 80, 255)
            vein_val = "轻度回流受阻"
            vein_color = (255, 180, 70, 255)
            nerve_val = f"{int(25*p)}% (被动牵张)"
            nerve_color = (255, 180, 70, 255)
            is_burst = False
        elif i <= 47:
            p = (i - 26) / 21.0
            prog = 1.0
            pulse = math.sin(p * math.pi * 4) * 0.08
            cur_d = round(6.7 + pulse, 1)
            cur_ax = int(3150 + math.sin(p * math.pi * 4) * 150)
            cur_iap = int(205 + math.sin(p * math.pi * 4) * 12)
            phase_desc = "动作：Valsalva 屏气用力排便 (腹压海啸式飙升，3200N 超载水锤暴击!)"
            axial_val = f"{cur_ax} N (超负荷)"
            axial_color = (255, 60, 60, 255)
            iap_val = f"{cur_iap} mmHg (高压)"
            iap_color = (255, 50, 50, 255)
            prot_val = f"{cur_d} mm (嵌顿暴突)"
            prot_color = (255, 50, 50, 255)
            vein_val = "Batson静脉怒张"
            vein_color = (255, 80, 80, 255)
            nerve_val = "82% (重度压扁形变)"
            nerve_color = (255, 60, 60, 255)
            is_burst = True
        else:
            p = (i - 47) / 12.0
            prog = 1.0 - p
            phase_desc = "动作：声门打开呼气，腹压骤降，轴向压力卸载"
            cur_ax = int(3200 - 2700 * p)
            cur_iap = int(205 - 190 * p)
            axial_val = f"{cur_ax} N (回落)"
            axial_color = (255, 160, 90, 255)
            iap_val = f"{cur_iap} mmHg (卸载)"
            iap_color = (255, 180, 80, 255)
            d = round(5.8 - 0.2 * p, 1)
            prot_val = f"{d} mm (回弹)"
            prot_color = (255, 160, 90, 255)
            vein_val = "充血逐渐消退"
            vein_color = (255, 200, 100, 255)
            nerve_val = f"{int(82 * (1 - p))}%"
            nerve_color = (255, 160, 90, 255)
            is_burst = (p < 0.3)

        current_slice = cropped_base.copy()
        overlay = Image.new("RGBA", current_slice.size, (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # 水锤暴压与静脉怒张视觉特效
        if is_burst:
            # 髓核中心高压水锤辐射波
            shock_r = int(48 + (i % 6) * 6)
            draw_ov.ellipse(
                [(prot_cx - shock_r, prot_cy - shock_r), (prot_cx + shock_r, prot_cy + shock_r)],
                outline=(255, 60, 60, 230), width=3
            )
            # 内部高温高压光晕
            for r in range(40, 10, -5):
                a = int(140 * (1.0 - (r - 10) / 30.0))
                draw_ov.ellipse(
                    [(prot_cx - r, prot_cy - r), (prot_cx + r, prot_cy + r)],
                    fill=(255, 50, 40, a)
                )
            # 神经根严重挤压与放电电弧
            draw_corner_brackets(draw_ov, nerve_cx, nerve_cy, sz=40, color=(255, 240, 70, 255), width=2)
            for ang in range(0, 360, 45):
                theta = math.radians(ang + (i * 20) % 360)
                px1 = nerve_cx + math.cos(theta) * 14
                py1 = nerve_cy + math.sin(theta) * 14
                px2 = nerve_cx + math.cos(theta) * 32
                py2 = nerve_cy + math.sin(theta) * 32
                draw_ov.line([(px1, py1), (px2, py2)], fill=(255, 255, 90, 240), width=2)
        elif prog > 0.1:
            r = int(25 + prog * 20)
            draw_ov.ellipse(
                [(prot_cx - r, prot_cy - r), (prot_cx + r, prot_cy + r)],
                fill=(230, 60, 60, int(90 * prog))
            )

        current_slice = Image.alpha_composite(current_slice, overlay)
        frame.paste(current_slice, (0, 62))

        # HUD 悬浮面板
        draw_hud = ImageDraw.Draw(frame)
        card_x, card_y = 20, 78
        card_w, card_h = 240, 130
        hud_lines = [
            ("合成轴向压:", axial_val, axial_color),
            ("腹内压(IAP):", iap_val, iap_color),
            ("突入椎管深度:", prot_val, prot_color),
            ("Batson静脉丛:", vein_val, vein_color),
            ("S1神经根压扁:", nerve_val, nerve_color),
        ]
        draw_glass_card(draw_hud, card_x, card_y, card_w, card_h, "【L5/S1 动态暴压遥测】", hud_lines, border_color=(255, 80, 80, 180) if is_burst else (0, 180, 240, 180))

        # 顶部标题栏
        draw_hud.rectangle([(0, 0), (target_w, 62)], fill=(12, 18, 26, 255))
        draw_hud.line([(0, 61), (target_w, 61)], fill=(35, 48, 68, 255), width=1)
        draw_hud.text((18, 8), "【L5/S1 横断面微观力学演变】蹲姿排便与 Valsalva: 水锤暴压与静脉怒张", font=FONT_TITLE, fill=(240, 245, 255))
        sub_color = (255, 90, 90) if is_burst else (150, 185, 225)
        draw_hud.text((18, 35), phase_desc, font=FONT_SUB, fill=sub_color)

        # 底部状态栏
        draw_hud.rectangle([(0, 537), (target_w, 600)], fill=(12, 18, 26, 255))
        draw_hud.line([(0, 537), (target_w, 537)], fill=(35, 48, 68, 255), width=1)

        line1_text = f"复合压应力: 3200 N (320kg重压) | 腹压传递: Batson静脉丛高压充血 | 髓核动力学: 牙膏喷射水锤效应"
        draw_hud.text((18, 544), line1_text, font=FONT_BOTTOM_LINE1, fill=(180, 205, 230))

        if is_burst:
            draw_warning_badge(draw_hud, 18, 570, size=15)
            alert_text = "致命高危警报: 突出物瞬间膨大至6.7mm，静脉怒张合围，神经灌注归零，存在纤维环急性破裂高危风险!"
            draw_hud.text((38, 569), alert_text, font=FONT_BOTTOM_LINE2, fill=(255, 80, 80))
        else:
            draw_hud.text((18, 569), "力学机理: 极限深蹲导致前窄后宽楔形变，Valsalva 闭气使髓核内压与脑脊液压力形成多重冲击波。", font=FONT_BOTTOM_LINE2, fill=(120, 165, 210))

        frames.append(frame.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG))

    out_path = os.path.join(OUTPUT_DIR, "axial_squat_valsalva_dynamic.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=40, loop=0)
    print(f"Generated {out_path}, size: {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    print("正在渲染葛优躺轴位动态 GIF (V2)...")
    render_geyou_gif()
    print("正在渲染蹲姿 Valsalva 轴位动态 GIF (V2)...")
    render_squat_gif()
    print("渲染完成！")
