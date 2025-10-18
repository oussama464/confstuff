
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    vault_enabled=True,
    vault_url = "",
    vault_token="",
    vault_kv_version=2,
    vault_path="demo",
    settings_files=['settings.toml', '.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

print(settings.APP_NAME)
print(settings.FOO)
print(settings.API_KEY)
