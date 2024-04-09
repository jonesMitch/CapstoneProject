import numpy as np

def threshold(img: np.ndarray, low_ratio: float, high_ratio: float, weak=np.int32(25)):

    high_threshold = img.max() * high_ratio
    low_threshold = high_threshold * low_ratio

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.int32)

    strong = np.int32(255)
    strong_i, strong_j = np.where(img >= high_threshold)
    weak_i, weak_j = np.where((img<=high_threshold) & (img >= low_threshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    for i in range(1, M-1):
        for j in range(1, N-1):
            if res[i, j] == weak:
                if (
                    (res[i+1, j-1] == strong) or (res[i+1, j] == strong) or
                    (res[i+1, j+1] == strong) or (res[i, j-1] == strong) or
                    (res[i, j+1] == strong) or (res[i-1, j-1] == strong) or
                    (res[i-1, j] == strong) or (res[i-1, j+1] == strong)
                ):
                    res[i, j] = strong
                else:
                    res[i, j] = 0
    return res