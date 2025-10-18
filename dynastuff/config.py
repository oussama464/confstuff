
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    vault_enabled=True,
    environment=True, # so u can switch env
    load_dotenv=True,
    settings_files=['settings.toml', '.secrets.toml'])

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
