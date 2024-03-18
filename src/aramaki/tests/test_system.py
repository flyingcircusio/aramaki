import uuid

import pytest_patterns.plugin
import transaction

from aramaki.models.system import Instance, System, SystemCategory


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

    assert len(infrastructure.systems) == 2
    assert subsystem in infrastructure.systems
    assert system in infrastructure.systems

    anchors = infrastructure.anchor_systems()
    assert len(anchors) == 1
    assert anchors[0] is system


def test_system_overview(
    testbrowser, dbsession, patterns: pytest_patterns.plugin.PatternsLib
):
    instance = Instance()
    infrastructure = SystemCategory("Infrastructure")

    dc1 = System(
        title="First data center",
        primary_instance=instance,
        category=infrastructure,
    )
    dbsession.add(dc1)

    dc2 = System(
        title="Second data center",
        primary_instance=instance,
        category=infrastructure,
    )
    dbsession.add(dc2)

    project = SystemCategory("Project")
    dbsession.add(project)

    p1 = System(
        title="First project",
        primary_instance=instance,
        category=project,
    )
    dbsession.add(p1)
    p2 = System(
        title="Second project",
        primary_instance=instance,
        category=project,
    )
    dbsession.add(p2)

    service = SystemCategory("Service")
    dbsession.add(service)

    s1 = System(
        title="First service",
        primary_instance=instance,
        category=service,
    )
    dbsession.add(s1)
    s2 = System(
        title="Second service",
        primary_instance=instance,
        category=service,
    )
    dbsession.add(s2)

    dbsession.flush()

    transaction.commit()

    testbrowser.open("http://example.com/")

    owrap = patterns.owrap
    owrap.optional("<empty-line>")
    owrap.optional("    ")
    owrap.optional("  ")
    owrap.optional("    <meta ...>")
    owrap.optional("    <script ...>")
    owrap.optional("    <link ...>")
    owrap.optional("    <!-- ...")
    owrap.in_order(
        """
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Aramaki</title>
  </head>
  <body ...>
    <nav ...>
      Aramaki
    </nav>
    <div ...>
    </div>
  </body>
</html>
"""
    )

    dashboard = patterns.dashboard
    dashboard.merge("owrap")
    dashboard.continuous(
        """
      <div>
        <h2 ...>Infrastructure</h2>

        <ul ...>
          <li>First data center</li>
          <li>Second data center</li>
        </ul>
      </div>
      <div>
        <h2 ...>Project</h2>

        <ul ...>
          <li>First project</li>
          <li>Second project</li>
        </ul>
      </div>
      <div>
        <h2 ...>Service</h2>

        <ul ...>
          <li>First service</li>
          <li>Second service</li>
        </ul>
      </div>
"""
    )

    assert dashboard == testbrowser.contents
