import pytest
import math
from render import volumetric_shadow as mod

CASES = [
    ("steps", 'm.shadow_steps(10, 2) == 5'),
    ("noise", 'm.blue_noise(0, 0, 0) == approx(0.0)'),
    ("reproj", 'm.reproject((0.5, 0.5), (0.1, 0.2)) == approx((0.6, 0.7))'),
    ("planes", 'm.unify_planes(0.1, 100) == (0.1, 100)'),
    ("density", 'm.density_scale(2, 3) == 6'),
    ("transparent", 'm.transparent_once(2) == 1'),
    ("step", 'm.adaptive_step(0.1, 2) == approx(0.2)'),
    ("temporal", 'm.temporal_alpha(0) == approx(1.0)'),
    ("fade", 'm.resolution_fade(1) == approx(0.5)'),
    ("inside", 'm.inside_light(0.5, 1) is True'),
    ("trans", 'm.transmittance(0, 5) == approx(1.0)'),
    ("offset", 'm.sample_offset(1, 4) == approx(0.25)'),
    ("key", 'm.vol_key("lamp", 2) == "lamp:2"'),
    ("lit", 'm.is_lit(0.5) is True'),
    ("clamp", 'm.clamp01(1.2) == 1.0')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
