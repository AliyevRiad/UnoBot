import time

class MWT(object):
    """Vaxtla məhdudlaşdırılmış yaddaş (cache) - Memoize With Timeout"""
    
    _caches = {}   # Bütün funksiyalar üçün yaddaş (keş) saxlanır
    _timeouts = {} # Hər funksiyaya uyğun vaxt limiti saxlanır

    def __init__(self, timeout=2):
        # Yaddaşdakı məlumat neçə saniyə etibarlı qalacaq
        self.timeout = timeout

    def collect(self):
        """Vaxtı keçmiş nəticələri keşdən təmizləyir"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                # Əgər nəticə hələ vaxtında etibarlıdırsa, saxla
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            # Təmizlənmiş yaddaşı geri yaz
            self._caches[func] = cache

    def __call__(self, f):
        # Funksiyanı büküb ona yaddaş (cache) əlavə edir
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())  # kwargs-ları sıraya düz
            key = (args, tuple(kw))      # argumentlərə əsasən unikal açar yarat

            try:
                v = self.cache[key]
                print("cache")  # Əgər nəticə yaddaşdadırsa, çap et
                # Vaxt keçibsə, yenidən hesablamaq üçün KeyError at
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                print("new")  # Yenidən hesablamaq lazımdır
                v = self.cache[key] = (f(*args, **kwargs), time.time())

            return v[0]  # Saxlanmış nəticəni qaytar

        func.func_name = f.__name__  # Orijinal funksiyanın adını saxla
        return func
