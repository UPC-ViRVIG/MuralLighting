import os
import subprocess
import tempfile

import mitsuba as mi
import numpy as np

mi.set_variant("scalar_rgb")

# =========================================================
# CONFIG
# =========================================================

INPUT_EXR = "../images/C1-ART_1.EXR"
OUTPUT_EXR = "denoised.exr"

OIDN_EXE = r"oidn\bin\oidnDenoise.exe"

CLAMP_VALUE = 20 # not used

# =========================================================
# PFM HELPERS
# =========================================================

def save_pfm(path, image):
    image = np.flipud(image)

    if image.dtype != np.float32:
        image = image.astype(np.float32)

    color = (image.ndim == 3 and image.shape[2] == 3)

    with open(path, "wb") as f:

        f.write(b"PF\n" if color else b"Pf\n")

        f.write(f"{image.shape[1]} {image.shape[0]}\n".encode())

        # little endian
        f.write(b"-1.0\n")

        image.tofile(f)


def load_pfm(path):
    with open(path, "rb") as f:
        header = f.readline().decode().rstrip()
        color = (header == "PF")
        w, h = map(int, f.readline().decode().split())
        scale = float(f.readline().decode())
        data = np.fromfile(f, "<f")
        shape = (h, w, 3) if color else (h, w)
        data = np.reshape(data, shape)
        data = np.flipud(data)
        return data.astype(np.float32)

# =========================================================
# READ EXR
# =========================================================

bmp = mi.Bitmap(INPUT_EXR)

#print(bmp.channel_names())

img = np.array(bmp).astype(np.float32)
print("Input shape:", img.shape)
h, w, c = img.shape

# ---------------------------------------------------------
# CHANNELS
# ---------------------------------------------------------
color = np.ascontiguousarray(img[..., 0:3], dtype=np.float32) # RGB samples

albedo = None
normal = None

if c >= 13:
    # per què 13?
    albedo = np.ascontiguousarray(img[..., 3:6], dtype=np.float32)
    normal = np.ascontiguousarray(img[..., 7:10], dtype=np.float32) # 10:13?
    print("Using color + albedo + normal")
else:
    print("No albedo/normal found; using color only.")

# =========================================================
# CLAMP
# =========================================================

lum = (
    0.2126 * color[..., 0] +
    0.7152 * color[..., 1] +
    0.0722 * color[..., 2]
)
print("Luminance max before clamp:", np.max(lum))

scale = np.minimum(1.0, CLAMP_VALUE / (lum + 1e-6))

color = np.ascontiguousarray(
    color * scale[..., None],
    dtype=np.float32
)

lum2 = (
    0.2126 * color[..., 0] +
    0.7152 * color[..., 1] +
    0.0722 * color[..., 2]
)

print("Luminance max after clamp:", np.max(lum2))

# =========================================================
# TEMP FILES
# =========================================================

tmpdir = tempfile.mkdtemp()

color_pfm = os.path.join(tmpdir, "color.pfm")
albedo_pfm = os.path.join(tmpdir, "albedo.pfm")
normal_pfm = os.path.join(tmpdir, "normal.pfm")
output_pfm = os.path.join(tmpdir, "output.pfm")

# =========================================================
# SAVE PFM
# =========================================================

save_pfm(color_pfm, color)

cmd = [
    OIDN_EXE,
    "-hdr", color_pfm,
    "-quality", "high"
]

if albedo is not None:
    save_pfm(albedo_pfm, albedo)

    cmd += [
        "-alb", albedo_pfm
    ]

if normal is not None:
    save_pfm(normal_pfm, normal)

    cmd += [
        "-nrm", normal_pfm
    ]

cmd += [
    "-o", output_pfm
]

# =========================================================
# RUN OIDN
# =========================================================

print("\nRunning OIDN:")
print(" ".join(cmd))

result = subprocess.run(
    cmd,
    capture_output=True,
    text=True
)

print(result.stdout)

if result.returncode != 0:
    print(result.stderr)
    raise RuntimeError("OIDN failed.")

# =========================================================
# LOAD RESULT
# =========================================================

output = load_pfm(output_pfm)

print("Output shape:", output.shape)
print("Output min/max:", np.min(output), np.max(output))

# =========================================================
# SAVE EXR
# =========================================================

mi.Bitmap(output).write(OUTPUT_EXR)

print("\nSaved:", OUTPUT_EXR)