import os
from collections import Counter
from multiprocessing import Pool

import numpy as np
from lppls import lppls

WORKERS = 8
WINDOW_SIZE = 120
SMALLEST_WINDOW_SIZE = 30
OUTER_INCREMENT = 2
INNER_INCREMENT = 1
MAX_SEARCHES = 25

# 캐시 파일의 파라미터와 다르면 캐시를 버리고 전체 재계산
PARAMS = np.array([WINDOW_SIZE, SMALLEST_WINDOW_SIZE, OUTER_INCREMENT, INNER_INCREMENT, MAX_SEARCHES])
FIT_KEYS = ["tc", "m", "w", "a", "b", "c", "c1", "c2", "t1", "t2", "O", "D"]


def _load_cache(cache_path):
    """캐시 파일 → ({t2: 윈도우 결과 dict}, 그리드 위 t2 집합). 없거나 파라미터가 다르면 빈 값."""
    if not cache_path or not os.path.exists(cache_path):
        return {}, set()
    try:
        data = np.load(cache_path)
        if not np.array_equal(data["params"], PARAMS):
            print(f"  cache params changed, full recompute: {cache_path}")
            return {}, set()
        cached = {}
        for t1, t2, p2, fits in zip(data["t1"].tolist(), data["t2"].tolist(),
                                    data["p2"].tolist(), data["fits"].tolist()):
            cached[t2] = {
                "t1": t1, "t2": t2, "p2": p2,
                "res": [dict(zip(FIT_KEYS, f)) for f in fits],
            }
        grid_t2 = set(data["t2"][data["grid"]].tolist())
        return cached, grid_t2
    except Exception as e:
        print(f"  cache load failed ({e}), full recompute: {cache_path}")
        return {}, set()


def _save_cache(cache_path, res, grid_t2):
    if not cache_path or not res:
        return
    os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
    tmp_path = cache_path + ".tmp.npz"
    np.savez_compressed(
        tmp_path,
        params=PARAMS,
        grid=np.array([r["t2"] in grid_t2 for r in res], dtype=bool),
        t1=np.array([r["t1"] for r in res], dtype=float),
        t2=np.array([r["t2"] for r in res], dtype=float),
        p2=np.array([r["p2"] for r in res], dtype=float),
        fits=np.array([[[f[k] for k in FIT_KEYS] for f in r["res"]] for r in res], dtype=float),
    )
    os.replace(tmp_path, cache_path)


def _is_valid(r, observations, end_idx):
    # 윈도우 시작일과 마지막 가격이 현재 데이터와 같아야 재사용 (액면분할 등으로 과거 가격이 바뀌면 재계산)
    times, prices = observations
    return (r["t1"] == times[end_idx - WINDOW_SIZE + 1]
            and np.isclose(r["p2"], prices[end_idx]))


def compute_lpplci(observations, cache_path=None):
    """LPPLS nested fit 결과를 계산한다.

    cache_path가 주어지면 이전 결과를 불러와 비어있는(최근) 윈도우만 새로 계산하고,
    결과를 다시 저장한다. 반환값은 lppls의 mp_compute_nested_fits와 같은 형식.
    """
    lppls_model = lppls.LPPLS(observations=observations)
    times = observations[0]
    n = len(times)
    first_end = WINDOW_SIZE - 1
    if n <= first_end:
        raise ValueError(f"데이터가 윈도우 크기({WINDOW_SIZE})보다 짧습니다: {n}")

    cached, cached_grid_t2 = _load_cache(cache_path)
    index_of = {t: i for i, t in enumerate(times.tolist())}

    # 윈도우 끝 인덱스 그리드: OUTER_INCREMENT 간격, 캐시가 있으면 캐시의 그리드 위상을 그대로 따른다
    grid_idx = [index_of[t2] for t2 in cached_grid_t2 if t2 in index_of]
    if grid_idx:
        phase = Counter(i % OUTER_INCREMENT for i in grid_idx).most_common(1)[0][0]
    else:
        phase = first_end % OUTER_INCREMENT
    grid = {i for i in range(first_end, n) if i % OUTER_INCREMENT == phase}
    # 그리드 + 최신 거래일(항상) + 이전에 계산해둔 그리드 밖 날짜(매일 실행분)
    extra = {index_of[t2] for t2 in cached if index_of.get(t2, -1) >= first_end}
    targets = sorted(grid | extra | {n - 1})
    grid_t2 = {times[i].item() for i in grid}

    res, todo = [], []
    for i in targets:
        r = cached.get(times[i].item())
        if r is not None and _is_valid(r, observations, i):
            res.append(r)
        else:
            todo.append(i)

    print(f"  windows: {len(targets)} total, {len(res)} cached, {len(todo)} to compute")

    if todo:
        # lppls 0.6.23 내부 워커 함수를 윈도우 단위로 직접 호출 (mp_compute_nested_fits와 동일한 인자)
        func_arg_map = [
            (
                observations[:, i - WINDOW_SIZE + 1 : i + 1],
                WINDOW_SIZE,
                i - WINDOW_SIZE + 1,
                SMALLEST_WINDOW_SIZE,
                OUTER_INCREMENT,
                INNER_INCREMENT,
                MAX_SEARCHES,
            )
            for i in todo
        ]
        with Pool(processes=min(WORKERS, len(func_arg_map))) as pool:
            res += pool.map(lppls_model._func_compute_nested_fits, func_arg_map)

    res.sort(key=lambda r: r["t2"])
    _save_cache(cache_path, res, grid_t2)
    lppls_model.indicator_result = res
    return lppls_model, res
