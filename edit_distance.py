import numpy as np


def edit_distance(s1: str, s2: str):
    D = np.zeros((len(s1) + 1, len(s2) + 1))
    path_memory = np.zeros((len(s1) + 1, len(s2) + 1), dtype=object)

    for i in range(1, len(s1) + 1):
        D[i, 0] = i
        path_memory[i, 0] = (-1, 0)

    for j in range(1, len(s2) + 1):
        D[0, j] = j
        path_memory[0, j] = (0, -1)

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                D[i, j] = D[i - 1, j - 1]
                path_memory[i, j] = (0, 0)
            else:
                possibilities = [1 + D[i - 1, j], 1 + D[i, j - 1], 1 + D[i - 1, j - 1]]
                min_pos = np.inf
                min_idx = np.inf
                for k in range(len(possibilities)):
                    if possibilities[k] < min_pos:
                        min_pos = possibilities[k]
                        min_idx = k
                D[i, j] = min_pos
                if min_idx == 0:
                    path_memory[i, j] = (-1, 0)
                elif min_idx == 1:
                    path_memory[i, j] = (0, -1)
                else:
                    path_memory[i, j] = (-1, -1)

    return int(D[-1, -1])
