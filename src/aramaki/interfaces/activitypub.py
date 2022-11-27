import aramaki.system

internal_routed_applications = {}


class InternalActivityPubRouter:
    def __init__(self, context):
        self.context = context
        internal_routed_applications[context.application_url] = self

    def send(self, object):
        for url, router in internal_routed_applications.items():
            if not object["to"].startswith(url):
                continue
            router.receive(object)
            break

    def receive(self, object):
        with self.context:
            for system in aramaki.system.System.list():
                if system.actor_id != object["to"]:
                    continue
                system.receive_usage_request(object)
                break
