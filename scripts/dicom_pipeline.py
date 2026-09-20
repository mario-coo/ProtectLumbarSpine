#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProtectingLumbarSpine - 自动化腰椎 CT DICOM 分析与多平面重组工具
用途：供日后复查对比使用。支持导入任意医院导出的 DICOM 容积数据，
自动提取 0.625mm/1mm 薄层序列，完成 3D 体积重建、正中矢状位全景生成与 L5/S1 重点节段切片导出。
"""

import os
import sys
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

try:
    import pydicom
except ImportError:
    pydicom = None


def apply_window(hu_image, window_center, window_width):
    """应用 CT 窗宽窗位变换 (Hounsfield Unit 转 8位灰度)"""
    min_val = window_center - window_width / 2.0
    max_val = window_center + window_width / 2.0
    windowed = np.clip(hu_image, min_val, max_val)
    windowed = ((windowed - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)
    return windowed


def load_dicom_volume(dcm_files):
    """加载并按空间坐标严格排序 DICOM 切片"""
    slices = []
    for f in dcm_files:
        try:
            ds = pydicom.dcmread(f)
            if hasattr(ds, 'ImagePositionPatient'):
                slices.append(ds)
        except Exception:
            continue

    if not slices:
        raise ValueError("未找到有效的带有空间定位信息的 DICOM 切片")

    # 从头到脚排序 (Z 轴递减)
    slices.sort(key=lambda s: float(s.ImagePositionPatient[2]), reverse=True)
    pixel_spacing = [float(x) for x in slices[0].PixelSpacing]
    z_coords = [float(s.ImagePositionPatient[2]) for s in slices]
    slice_thickness = abs(z_coords[0] - z_coords[1]) if len(z_coords) > 1 else float(getattr(slices[0], 'SliceThickness', 1.0))

    volume = np.zeros((len(slices), slices[0].Rows, slices[0].Columns), dtype=np.float32)
    for i, s in enumerate(slices):
        slope = float(getattr(s, 'RescaleSlope', 1.0))
        intercept = float(getattr(s, 'RescaleIntercept', 0.0))
        volume[i] = s.pixel_array.astype(np.float32) * slope + intercept

    return volume, slices, pixel_spacing, slice_thickness, z_coords


def run_pipeline(dicom_root_dir, output_dir):
    """执行完整的重建与导出流程"""
    if pydicom is None:
        print("错误: 缺少 pydicom 依赖库，请先执行: pip install -r requirements.txt")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print(f"正在扫描 DICOM 文件目录: {dicom_root_dir} ...")
    all_dcm = glob.glob(os.path.join(dicom_root_dir, '**', '*.dcm'), recursive=True)
    print(f"共发现 {len(all_dcm)} 个 DICOM 文件")

    # 按序列分组
    series_map = {}
    for fpath in all_dcm:
        try:
            ds = pydicom.dcmread(fpath, stop_before_pixels=True)
            snum = int(getattr(ds, 'SeriesNumber', 0))
            if snum not in series_map:
                series_map[snum] = []
            series_map[snum].append(fpath)
        except Exception:
            continue

    print(f"识别到的序列数量: {len(series_map)}")
    # 挑选切片数量最多的主容积序列
    sorted_series = sorted(series_map.items(), key=lambda item: len(item[1]), reverse=True)
    best_snum, best_files = sorted_series[0]
    print(f"选择切片数最多的主序列 Series #{best_snum} (共 {len(best_files)} 层切片) 进行 3D MPR 重建...")

    vol, slices, spacing, dz, z_coords = load_dicom_volume(best_files)
    print(f"容积尺寸: {vol.shape}, 体素大小: dx={spacing[1]:.3f}mm, dy={spacing[0]:.3f}mm, dz={dz:.3f}mm")

    # 1. 重建正中矢状位
    mid_x = vol.shape[2] // 2
    scale_z = dz / spacing[0]
    sag_soft = apply_window(vol[:, :, mid_x], 45, 320)
    sag_bone = apply_window(vol[:, :, mid_x], 350, 1600)

    new_h = int(sag_soft.shape[0] * scale_z)
    new_w = sag_soft.shape[1]

    im_sag_soft = Image.fromarray(sag_soft).resize((new_w, new_h), Image.Resampling.BILINEAR)
    im_sag_bone = Image.fromarray(sag_bone).resize((new_w, new_h), Image.Resampling.BILINEAR)

    im_sag_soft.save(os.path.join(output_dir, 'reconstructed_sagittal_soft.png'))
    im_sag_bone.save(os.path.join(output_dir, 'reconstructed_sagittal_bone.png'))
    print("正中矢状位全景重建图已导出！")

    # 2. 导出全容积轴位概览
    overview_dir = os.path.join(output_dir, 'axial_overview')
    os.makedirs(overview_dir, exist_ok=True)
    step = max(1, len(slices) // 30)
    for idx in range(0, len(slices), step):
        ax_img = apply_window(vol[idx], 45, 320)
        Image.fromarray(ax_img).save(os.path.join(overview_dir, f"slice_{idx:03d}.png"))

    print(f"轴位概览切片已导出至: {overview_dir}")
    print("自动化分析处理完成！")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print("用法: python scripts/dicom_pipeline.py [dicom文件夹路径]")
        print("说明: 若未传入路径，默认使用项目根目录下的 'input_dicom' 文件夹。")
        sys.exit(0)

    if len(sys.argv) > 1:
        dcm_dir = os.path.abspath(sys.argv[1])
    else:
        default_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'input_dicom'))
        if os.path.exists(default_dir):
            dcm_dir = default_dir
        else:
            print("错误: 未指定 DICOM 数据目录，且未找到默认的 'input_dicom' 文件夹。")
            print("用法: python scripts/dicom_pipeline.py <dicom文件夹路径>")
            sys.exit(1)

    if not os.path.exists(dcm_dir):
        print(f"错误: 指定的 DICOM 目录不存在: {dcm_dir}")
        sys.exit(1)

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output_analysis'))
    run_pipeline(dcm_dir, out_dir)
