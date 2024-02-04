import uuid

from aramaki.server.models.system import System, SystemCategory


def test_system_basic():
    infrastructure = SystemCategory("Infrastructure")
    assert infrastructure.title == "Infrastructure"
    assert isinstance(infrastructure.id, uuid.UUID)

    system = System(
        category=infrastructure,
        primary_instance="asdf",
        title="A system",
    )

    assert isinstance(system.id, uuid.UUID)
    assert system.title == "A system"
    assert system.primary_instance == "asdf"
    assert system.subsystems == []
    assert system.category == infrastructure
    assert system.category.title == "Infrastructure"

    subsystem = System(
        category=infrastructure,
        primary_instance="asdf",
        title="A subsystem",
    )
    system.subsystems.append(subsystem)

    assert system.subsystems == [subsystem]
