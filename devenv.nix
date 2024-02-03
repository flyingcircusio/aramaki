{ pkgs, lib, config, ... }:

{
  env.PYTHONUNBUFFERED = "true";
  env.ALEMBIC_CONFIG = "development.ini";
  env.PGDATABASE = "aramaki";
  env.MYPYPATH="stubs";

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

  scripts.db-revision.exec = ''
    alembic revision --autogenerate -m "''${1?need revision comment}"
  '';

  scripts.db-upgrade.exec = ''
    alembic upgrade head
  '';

  scripts.aramaki-web.exec = ''
    pserve development.ini
  '';

  enterShell = ''
        echo
      echo 🦾 Helper scripts you can run to make your development richer:
      echo 🦾
      ${pkgs.gnused}/bin/sed -e 's| |••|g' -e 's|=| |' <<EOF | ${pkgs.util-linuxMinimal}/bin/column -t | ${pkgs.gnused}/bin/sed -e 's|^|🦾 |' -e 's|••| |g'
      ${lib.generators.toKeyValue {} (lib.mapAttrs (name: value: value.description) config.scripts)}
      EOF
      echo
  '';

  processes = {
    # aramaki-server-web.exec = "pserve development.ini";
    # aramaki-server-processing.exec = "aramaki-server processing";
    # aramaki-server-federation.exec = "aramaki-server federation";
    # aramaki-server-agent-manager.exec = "aramaki-server agent-manager";
    # aramaki-agent.exec = "aramaki-agent";

    tailwindcss.exec = "cd tailwind; (while true; do sleep 10; done) | tailwindcss -i aramaki.css -o ../src/aramaki/server/web/static/aramaki.css --minify --watch";
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
