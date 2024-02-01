{ pkgs, ... }:

{
  env.PYTHONUNBUFFERED = "true";

  packages = [
    pkgs.git
    pkgs.postgresql_15
    pkgs.python311Packages.psycopg2
    pkgs.tailwindcss
  ];

  languages.python = {
    enable  = true;
    package = pkgs.python311Full;
    poetry = {
      enable = true;
      install = {
         enable = true;
         installRootPackage = true;
      };
    };
  };

  processes = {
    aramaki-server-ui.exec = "pserve development.ini";
    #aramaki-server-processing.exec = "aramaki-server processing";
    #aramaki-server-federation.exec = "aramaki-server federation";
    #aramaki-server-agent-manager.exec = "aramaki-server agent-manager";
    #    aramaki-agent.exec = "aramaki-agent";

    tailwindcss.exec = "cd tailwind; (while true; do sleep 10; done) | tailwindcss -i aramaki.css -o ../src/aramaki/server/ui/static/aramaki.css --minify --watch";
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

}
