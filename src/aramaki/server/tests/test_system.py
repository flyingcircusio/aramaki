import uuid

from aramaki.server.models.system import Instance, System, SystemCategory


def test_system_basic():
    instance = Instance()

    infrastructure = SystemCategory("Infrastructure")
    assert infrastructure.title == "Infrastructure"
    assert isinstance(infrastructure.id, uuid.UUID)

    system = System(
        category=infrastructure,
        primary_instance=instance,
        title="A system",
    )

    assert isinstance(system.id, uuid.UUID)
    assert system.title == "A system"
    assert system.primary_instance is instance
    assert system.subsystems == []
    assert system.category == infrastructure
    assert system.category.title == "Infrastructure"

    subsystem = System(
        category=infrastructure,
        primary_instance=instance,
        title="A subsystem",
    )
    system.subsystems.append(subsystem)

    assert system.subsystems == [subsystem]
