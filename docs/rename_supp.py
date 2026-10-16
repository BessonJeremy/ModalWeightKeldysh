#!/usr/bin/env python3
"""Rename supplementary-material files to journal-safe names
and update their references in the given text files (.qmd / .html)."""
import shutil
import sys
from pathlib import Path

RENAMES = {
    # Schwarzschild
    "activation_N=600_case=Schwarzschild-Zerilli_ell=2_precision=800_s=2_inset_version.mp4": "schw_zer_anim_inset.mp4",
    "activation_N=600_case=Schwarzschild_ell=2_precision=800_s=2_inset_version.mp4": "schw_rw_anim_inset.mp4",
    "activation_N=600_case=Schwarzschild-Zerilli_ell=2_precision=800_s=2_usual_gaussian_and_foreground.mp4": "schw_zer_anim.mp4",
    "activation_N=600_case=Schwarzschild_ell=2_precision=800_s=2_RW.mp4": "schw_rw_anim.mp4",
    "N=600_case=Schwarzschild-Zerilli_ell=2_precision=800_s=2_square_peaks.svg": "schw_zer_weight.svg",
    "N=600_case=Schwarzschild_ell=2_precision=800_s=2_square_peaks.svg": "schw_rw_weight.svg",
    "N=600_case=Schwarzschild-Zerilli_ell=2_precision=800_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "schw_zer_log.svg",
    "N=600_case=Schwarzschild_ell=2_precision=800_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "schw_rw_log.svg",
    # Reissner-Nordström, Q/M = 0.01
    "activation_M=1_N=400_Q=0.01_case=RN-Zerilli_ell=2_precision=500_s=2_foreground.mp4": "rn_q001_zer_anim.mp4",
    "activation_M=1_N=400_Q=0.01_case=RN-RW_ell=2_precision=500_s=2_foreground.mp4": "rn_q001_rw_anim.mp4",
    "M=1_N=400_Q=0.01_case=RN-Zerilli_ell=2_precision=500_s=2_square_peaks.svg": "rn_q001_zer_weight.svg",
    "M=1_N=400_Q=0.01_case=RN-RW_ell=2_precision=500_s=2_square_peaks.svg": "rn_q001_rw_weight.svg",
    "M=1_N=400_Q=0.01_case=RN-Zerilli_ell=2_precision=500_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "rn_q001_zer_log.svg",
    "M=1_N=400_Q=0.01_case=RN-RW_ell=2_precision=500_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "rn_q001_rw_log.svg",
    # Reissner-Nordström, Q/M = 0.1
    "activation_M=1_N=400_Q=0.1_case=RN-Zerilli_ell=2_precision=500_s=2_foreground.mp4": "rn_q01_zer_anim.mp4",
    "activation_M=1_N=400_Q=0.1_case=RN-RW_ell=2_precision=500_s=2_foreground.mp4": "rn_q01_rw_anim.mp4",
    "M=1_N=400_Q=0.1_case=RN-Zerilli_ell=2_precision=500_s=2_square_peaks.svg": "rn_q01_zer_weight.svg",
    "M=1_N=400_Q=0.1_case=RN-RW_ell=2_precision=500_s=2_square_peaks.svg": "rn_q01_rw_weight.svg",
    "M=1_N=400_Q=0.1_case=RN-Zerilli_ell=2_precision=500_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "rn_q01_zer_log.svg",
    "M=1_N=400_Q=0.1_case=RN-RW_ell=2_precision=500_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "rn_q01_rw_log.svg",
    # Reissner-Nordström, Q/M = sqrt(7)/4
    "activation_M=1_N=400_Q=0.6614378277661477_case=RN-Zerilli_ell=2_precision=500_s=2_foreground.mp4": "rn_q066_zer_anim.mp4",
    "activation_M=1_N=400_Q=0.6614378277661477_case=RN-RW_ell=2_precision=500_s=2_foreground.mp4": "rn_q066_rw_anim.mp4",
    "M=1_N=400_Q=0.6614378277661477_case=RN-Zerilli_ell=2_precision=500_s=2_square_peaks.svg": "rn_q066_zer_weight.svg",
    "M=1_N=400_Q=0.6614378277661477_case=RN-RW_ell=2_precision=500_s=2_square_peaks.svg": "rn_q066_rw_weight.svg",
    "M=1_N=400_Q=0.6614378277661477_case=RN-Zerilli_ell=2_precision=500_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "rn_q066_zer_log.svg",
    "M=1_N=400_Q=0.6614378277661477_case=RN-RW_ell=2_precision=500_s=2_enveloping_log_long_first_10_seconds_zoom_2.svg": "rn_q066_rw_log.svg",
    # Schwarzschild-de Sitter
    "activation_Lambda=0.07_M=1_N=400_case=SdS-Zerilli-CORRECTED_ell=2_precision=500_s=2_foreground.mp4": "sds_zer_anim.mp4",
    "activation_Lambda=0.07_M=1_N=400_case=SdS-RW-CORRECTED_ell=2_precision=500_s=2_foreground.mp4": "sds_rw_anim.mp4",
    "Lambda=0.07_M=1_N=400_case=SdS-Zerilli-CORRECTED_ell=2_precision=500_s=2_.svg": "sds_zer_log.svg",
    "Lambda=0.07_M=1_N=400_case=SdS-RW-CORRECTED_ell=2_precision=500_s=2.svg": "sds_rw_log.svg",
    "Lambda=0.07_M=1_N=400_case=SdS-Zerilli-CORRECTED_ell=2_precision=500_s=2_enveloping_log_many.svg": "sds_zer_log_many.svg",
    "Lambda=0.07_M=1_N=400_case=SdS-RW-CORRECTED_ell=2_precision=500_s=2_enveloping_log_many.svg": "sds_rw_log_many.svg",
    # Kerr, a/M = 0.01
    "test_Kerr_activation_modes_a=0.01_m=0_centered_x_2d_gaussian_s=-2.mp4": "kerr_a001_sm2_anim.mp4",
    "test_Kerr_activation_modes_a=0.01_m=0_centered_x_2d_gaussian_s=+2.mp4": "kerr_a001_sp2_anim.mp4",
    "kerr_a=0.01_s=-2_square_peaks.svg": "kerr_a001_sm2_weight.svg",
    "kerr_a=0.01_s=+2_square_peaks.svg": "kerr_a001_sp2_weight.svg",
    "kerr_a=0.01_s=-2_enveloping_log_long_first_10_seconds_zoom_2.svg": "kerr_a001_sm2_log.svg",
    "kerr_a=0.01_s=+2_enveloping_log_long_first_10_seconds_zoom_2_text2_many.svg": "kerr_a001_sp2_log.svg",
    # Kerr, a/M = 0.1
    "test_Kerr_activation_modes_a=0.1_m=0_centered_x_2d_gaussian_s=-2.mp4": "kerr_a01_sm2_anim.mp4",
    "test_Kerr_activation_modes_a=0.1_m=0_centered_x_2d_gaussian_s=+2.mp4": "kerr_a01_sp2_anim.mp4",
    "kerr_a=0.1_s=-2_square_peaks.svg": "kerr_a01_sm2_weight.svg",
    "kerr_a=0.1_s=+2_square_peaks.svg": "kerr_a01_sp2_weight.svg",
    "kerr_a=0.1_s=-2_enveloping_log_long_first_10_seconds_zoom_2.svg": "kerr_a01_sm2_log.svg",
    "kerr_a=0.1_s=+2_enveloping_log_long_first_10_seconds_zoom_2.svg": "kerr_a01_sp2_log.svg",
}


def rename_files(folder, *text_files):
    """Rename the media files in `folder`, then replace the old names
    in each text file (a .bak backup of each text file is kept)."""
    folder = Path(folder)
    for old, new in RENAMES.items():
        src = folder / old
        if src.exists():
            src.rename(folder / new)
        else:
            print(f"not found, skipped: {old}")

    for f in map(Path, text_files):
        shutil.copy(f, f.with_name(f.name + ".bak"))
        text = f.read_text(encoding="utf-8")
        for old in sorted(RENAMES, key=len, reverse=True):  # longest first, to be safe
            text = text.replace(old, RENAMES[old])
        f.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    rename_files(sys.argv[1], *sys.argv[2:])
