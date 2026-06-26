import numpy as np
from robotrace.perturbations import PerturbationSpec, apply_visual_perturbation, perturbation_manifest
from robotrace.instruction_perturbations import perturb_instruction

def test_brightness_perturbation_changes_image():
    image = np.ones((8, 8, 3), dtype=np.uint8) * 100
    out = apply_visual_perturbation(image, PerturbationSpec("brightness", 0.5))
    assert out.shape == image.shape
    assert out.dtype == image.dtype
    assert float(out.mean()) > float(image.mean())

def test_blur_perturbation_shape_dtype():
    image = np.zeros((8, 8, 3), dtype=np.uint8)
    image[4, 4] = 255
    out = apply_visual_perturbation(image, PerturbationSpec("blur", 1.0))
    assert out.shape == image.shape
    assert out.dtype == image.dtype

def test_manifest_contains_expected_items():
    names = {item["name"] for item in perturbation_manifest()}
    assert "brightness" in names
    assert "contrast" in names
    assert "resolution_drop" in names

def test_instruction_perturbations_are_deterministic():
    text = "pick the red block and place it near the cup"
    variants = perturb_instruction(text)
    names = [v.name for v in variants]
    assert "original" in names
    assert "shortened" in names
    assert "object_masking" in names
    assert len(variants) >= 5
    assert any("[OBJECT]" in v.text for v in variants)
