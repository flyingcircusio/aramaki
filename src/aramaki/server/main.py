import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="aramaki-server",
        description="Server implementation of Aramaki, the federated DevOps "
        "control plane.",
        epilog="Text at the bottom of help",
    )

    parser.add_argument("subsystem")

    args = parser.parse_args()
    if args.subsystem == "processing":
        from .processing.main import main as real_main
    elif args.subsystem == "federation":
        from .federation.main import main as real_main
    elif args.subsystem == "agent-manager":
        from .agentmanager.main import main as real_main
    else:
        raise ValueError(args.subsystem)
    real_main()
