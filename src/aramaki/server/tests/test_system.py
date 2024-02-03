from aramaki.server.models.system import System


def test_system_basic():
    system = System()

    assert system.id is None
    assert system.title is None
    assert system.type_ is None
    assert system.primary_instance is None
