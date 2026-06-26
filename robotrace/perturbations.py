from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict
import numpy as np

@dataclass(frozen=True)
class PerturbationSpec:
    name: str
    severity: float
    params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "severity": float(self.severity), "params": dict(self.params)}

def _clip_like_original(arr: np.ndarray, original_dtype: Any, original_max: float) -> np.ndarray:
    arr = np.clip(arr, 0.0, original_max)
    if np.issubdtype(original_dtype, np.integer):
        return np.rint(arr).astype(original_dtype)
    return arr.astype(original_dtype)

def _normalize_image(image: Any):
    arr = np.asarray(image)
    if arr.ndim not in (2, 3):
        raise ValueError(f"image must be HxW or HxWxC, got shape {arr.shape}")
    original_dtype = arr.dtype
    original_max = 255.0 if np.issubdtype(original_dtype, np.integer) else 1.0
    return arr.astype(np.float32), original_dtype, original_max

def _resize_nearest(image: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    h, w = image.shape[:2]
    if h == out_h and w == out_w:
        return image.copy()
    y_idx = np.clip(np.round(np.linspace(0, h - 1, out_h)).astype(int), 0, h - 1)
    x_idx = np.clip(np.round(np.linspace(0, w - 1, out_w)).astype(int), 0, w - 1)
    return image[y_idx][:, x_idx]

def _box_blur(image: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return image.copy()
    pad = int(radius)
    if image.ndim == 2:
        padded = np.pad(image, ((pad, pad), (pad, pad)), mode="edge")
        out = np.zeros_like(image, dtype=np.float32)
        for dy in range(2 * pad + 1):
            for dx in range(2 * pad + 1):
                out += padded[dy:dy + image.shape[0], dx:dx + image.shape[1]]
        return out / float((2 * pad + 1) ** 2)
    padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
    out = np.zeros_like(image, dtype=np.float32)
    for dy in range(2 * pad + 1):
        for dx in range(2 * pad + 1):
            out += padded[dy:dy + image.shape[0], dx:dx + image.shape[1], :]
    return out / float((2 * pad + 1) ** 2)

def apply_visual_perturbation(image: Any, spec: PerturbationSpec) -> np.ndarray:
    arr, dtype, maxv = _normalize_image(image)
    sev = float(spec.severity)
    name = spec.name
    if name == "brightness":
        out = arr + sev * 0.35 * maxv
    elif name == "contrast":
        mean = np.mean(arr, axis=(0, 1), keepdims=True)
        out = (arr - mean) * (1.0 + sev) + mean
    elif name == "blur":
        out = _box_blur(arr, radius=int(max(1, round(sev))))
    elif name == "jpeg":
        quality = float(spec.params.get("quality", max(1.0, 100.0 * (1.0 - sev))))
        levels = int(np.clip(quality, 8, 100))
        bins = max(4, int(levels / 4))
        out = np.round(arr / maxv * bins) / bins * maxv
    elif name == "random_occlusion":
        h, w = arr.shape[:2]
        frac = float(np.clip(sev, 0.0, 0.9))
        oh = max(1, int(h * frac))
        ow = max(1, int(w * frac))
        y0 = max(0, (h - oh) // 2)
        x0 = max(0, (w - ow) // 2)
        out = arr.copy()
        out[y0:y0 + oh, x0:x0 + ow] = float(np.mean(arr))
    elif name == "center_crop":
        h, w = arr.shape[:2]
        keep = float(np.clip(sev, 0.1, 1.0))
        ch = max(1, int(h * keep))
        cw = max(1, int(w * keep))
        y0 = max(0, (h - ch) // 2)
        x0 = max(0, (w - cw) // 2)
        out = _resize_nearest(arr[y0:y0 + ch, x0:x0 + cw], h, w)
    elif name == "resolution_drop":
        h, w = arr.shape[:2]
        scale = float(np.clip(sev, 0.05, 1.0))
        small = _resize_nearest(arr, max(1, int(h * scale)), max(1, int(w * scale)))
        out = _resize_nearest(small, h, w)
    else:
        raise ValueError(f"unknown visual perturbation: {name}")
    return _clip_like_original(out, dtype, maxv)

def perturbation_manifest() -> list[dict]:
    return [
        PerturbationSpec("brightness", 0.2).to_dict(),
        PerturbationSpec("brightness", 0.5).to_dict(),
        PerturbationSpec("contrast", 0.2).to_dict(),
        PerturbationSpec("contrast", 0.5).to_dict(),
        PerturbationSpec("blur", 1.0).to_dict(),
        PerturbationSpec("jpeg", 0.5, {"quality": 50}).to_dict(),
        PerturbationSpec("random_occlusion", 0.2).to_dict(),
        PerturbationSpec("center_crop", 0.75).to_dict(),
        PerturbationSpec("resolution_drop", 0.5).to_dict(),
    ]
