from installer import OSInstaller
import uuid
import pytest


class TestOSPackageInstaller:

    def test_mac_os_installer_fake_path(self):
        with pytest.raises(SystemExit):
            path = str(uuid.uuid4())
            OSInstaller.install_homebrew_packages(path)

    def test_fail_mac_os_in_linux(self):
        path = './tests/unit/assets/brew_mock'
        assert False is OSInstaller.install_homebrew_packages(path, timeout=1)
