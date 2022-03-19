from app import App


class TestApp:
    def test_init(self):
        app = App()
        assert isinstance(app, App)

    def test_parse_opt_fake(self):
        app = App()
        res = app.parse_opt('not_exists')
        assert res is None

    def test_parse_opt(self):
        app = App()
        res = app.parse_opt('create')
        assert res is not None

    def test_create(self):
        pass

    def test_resync(self):
        pass

    def test_install(self):
        pass
