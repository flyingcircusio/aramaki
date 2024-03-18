from aramaki.models.observation import Observation
from aramaki.models.probe import Probe


def handle_systemd(uow, probe):
    if not isinstance(probe, Probe):
        return
    if probe.name != "systemd":
        return


def handle_systemd_unit_list(uow, probe):
    if not isinstance(probe, Probe):
        return
    if probe.name != "systemd-unit-list":
        return

    # when the list changes: delete / deactivate old observations? trigger
    # expire event?


def handle_systemd_unit(uow, probe):
    if not isinstance(probe, Probe):
        return
    if probe.name != "systemd-unit":
        return


def handle_load(uow, probe):
    pass


def handle_keepalive(uow, probe):
    pass


def handle_ping(uow, probe):
    if not isinstance(probe, Probe):
        return
    if probe.name != "ping":
        return
    # XXX move record to uow repository pattern?
    Observation.record(
        uow,
        system_id=probe["system"],
        name="ping",
        data={"value": probe["value"]},
    )


def observe_high_ping(uow, observation):
    if not isinstance(observation, Observation):
        return
    if not observation.name == "ping":
        return
    # XXX helper type to allow accessing dict keys
    # by attribute name?
    if observation.data["value"] > 500:
        observation.tag(uow, "error")


def alert_on_error(uow, observation):
    if not isinstance(observation, Observation):
        return
    if "error" in observation.tags:
        print(f"ERROR: {observation}")

    # Create/activate an alert object
    # Deactivate an existing alert object


def process(uow, event):
    for handler in [
        handle_systemd,
        handle_systemd_unit_list,
        handle_load,
        handle_keepalive,
        handle_ping,
        observe_high_ping,
        alert_on_error,
    ]:
        handler(uow, event)
