from lppls import lppls

def compute_lpplci(observations, lppls):
    MAX_SEARCHES = 25
    lppls_model = lppls.LPPLS(observations=observations)
    res = lppls_model.mp_compute_nested_fits(
        workers=8,
        window_size=120,
        smallest_window_size=30,
        outer_increment=2,
        inner_increment=2,
        max_searches=25,
    )
    return lppls_model, res 