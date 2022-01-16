class SkautisApi:
    def init_app(self, app):
        from skautis import SkautisApi as _SkautisApi

        appId = app.config.setdefault("SKAUTIS_APPID", None)
        test = app.config.setdefault("SKAUTIS_TEST", False)

        self._skautis = _SkautisApi(appId, test)

    def __getattr__(self, name):
        return getattr(self._skautis, name)
