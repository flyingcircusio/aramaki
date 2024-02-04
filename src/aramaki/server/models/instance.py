from . import meta


class Instance(meta.UIDBase):
    """An Aramaki instance.

    XXX We're still sketching this out.

    Instances are basically independent aramaki servers
    which talk to each other to federate systems.

    """

    __tablename__ = "instance"
