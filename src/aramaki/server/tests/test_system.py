import uuid

from aramaki.server.models.system import System


def test_system_basic():
    system = System(
        type_="infrastructure", primary_instance="asdf", title="A system"
    )

    assert isinstance(system.id, uuid.UUID)
    assert system.title == "A system"
    assert system.type_ == "infrastructure"
    assert system.primary_instance == "asdf"
    assert system.subsystems == []

    subsystem = System(
        type_="infrastructure", primary_instance="asdf", title="A subsystem"
    )
    system.subsystems.append(subsystem)

    assert system.subsystems == [subsystem]
