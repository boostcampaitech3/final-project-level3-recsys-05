class dotdict(dict):
    """_summary_

    dot.notation access to dictionary attributes

    Args:
        dict (_type_): dot을 이용하여 dictionary value에 접근할 수 있도록 하는 모듈
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
