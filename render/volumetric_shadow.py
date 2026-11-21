import math


def shadow_steps(depth, step):
    """采样步数：按深度和步长计算射线步进次数（多级深度采样共用）。"""
    if step <= 0:
        raise ValueError("step must be positive")
    return int(math.ceil(depth / step))


def blue_noise(x, y, frame):
    """蓝噪声偏移：按像素与帧序号生成 [0,1) 抖动，时域上逐帧变化以收敛。"""
    h = math.sin(x * 12.9898 + y * 78.233 + frame * 37.719) * 43758.5453
    return h - math.floor(h)


def reproject(uv, motion):
    """重投影：用运动矢量把当前帧 uv 映射回上一帧，供时域累积采样历史。"""
    return (uv[0] + motion[0], uv[1] + motion[1])


def unify_planes(near, far):
    """近远平面统一：阴影图与参与介质共用同一组裁剪面，返回统一后的 (near, far)。"""
    if near <= 0 or far <= near:
        raise ValueError("require 0 < near < far")
    return (near, far)


def density_scale(density, time):
    """密度缩放：密度采样坐标随光源移动更新后，按时间因子缩放。"""
    return density * time


def transparent_once(layers):
    """透明只算一次：半透明层既写深度又参与阴影时去重，每层只计一次透过率。"""
    if layers <= 0:
        return 0
    return (layers + 1) // 2


def adaptive_step(base, slope):
    """自适应步长：按深度斜率放大步长，掠射角处加密、平直处放疏。"""
    return base * slope


def temporal_alpha(frame):
    """时域收敛：累积权重随帧数递减，静止画面逐渐收敛不再闪烁。"""
    return 1.0 / (frame + 1)


def resolution_fade(level):
    """分辨率渐变：相邻阴影图档位之间按 2^-level 混合，切档不跳变。"""
    return 2.0 ** (-level)


def inside_light(distance, radius):
    """灯内判定：光源在介质内部时单独处理，不做正面剔除。"""
    return distance < radius


def transmittance(density, distance):
    """透过率：Beer-Lambert 衰减。"""
    return math.exp(-density * distance)


def sample_offset(index, count):
    """采样偏移：第 index 个样本在 count 级深度中的归一化位置。"""
    if count <= 0:
        raise ValueError("count must be positive")
    return index / count


def vol_key(seed, index):
    """体积阴影键：每盏灯独立的缓冲键，避免多灯互相覆盖。"""
    return f"{seed}:{index}"


def is_lit(energy):
    """能量判定：透过率大于零即受光。"""
    return energy > 0


def clamp01(value):
    """归一钳制到 [0, 1]。"""
    return max(0.0, min(1.0, value))
