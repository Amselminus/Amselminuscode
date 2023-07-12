from project_test import Create_Account

def test_get_password():
    c = Create_Account()
    assert c.get_password("Laurin_1601") == True




"""
class TestClass:

    def test_name(self):
        a = Account()
        set_keyboard_input(["laurin"])
        a.get_name()
        output = get_display_output
        assert output == ["Laurin"]


def test_name():
    a = Account()
    assert a.get_name() == "Laurin"


def test_address():
    a = Account()
    assert a.get_address("alpenblick 3, 83355 Grabenstaett") == "Alpenblick 3, 83355 Grabenstaett"
    assert a.get_address("alpenblick3, 83355 Grabenstaett") != "Alpenblick 3, 83355 Grabenstaett"

def test_birth():
    a = Account()
    assert a.get_birth("2004-01-16") == "2004-01-16"
    assert a.get_birth("200401-16") != "2004-01-16"
    assert a.get_birth("2004-01-40") != "2004-01-16"


def test_email():
    a = Account()
    assert a.get_email("laurin.boeger@web.de") == "laurin.boeger@web.de"
    assert a.get_email("laurin@boeger.net") == "laurin@boeger.net"
    assert a.get_email("laurin@boeger.adfs.net") == "laurin@boeger.adfs.net"
    assert a.get_email("laurin@boeger@web.de") != "laurin.boeger@web.de"
"""