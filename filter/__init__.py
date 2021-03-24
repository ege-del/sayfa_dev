from .filter_low_quality.main import _filter as _filter_low_quality

algos = {
    'low_quality':_filter_low_quality,
}
