{ pkgs, ... }:

{
  env.PYTHONUNBUFFERED = "true";

  packages = [
    pkgs.git
    pkgs.postgresql_15
    pkgs.python311Packages.psycopg2
  ];

  enterShell = ''
    pip install -e ./
  '';

  languages.python = {
    enable  = true;
    package = pkgs.python311Full;
    venv = { 
      enable = true;
      quiet = true;
    };
  };

  processes = {
    aramaki-server-ui.exec = "aramaki-server ui";
    aramaki-server-processing.exec = "aramaki-server processing";
    aramaki-server-federation.exec = "aramaki-server federation";
    aramaki-server-agent-manager.exec = "aramaki-server agent-manager";
  
    aramaki-agent.exec = "aramaki-agent";
  };

  services.postgres = {
    enable = true;
    package = pkgs.postgresql_15;
    initialDatabases = [{ name = "aramaki"; }];
  };

  services.redis.enable = true;

  pre-commit.hooks = {
    shellcheck.enable = true;
    black.enable = true;
    isort.enable = true;
    ruff.enable = true;
  };

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
