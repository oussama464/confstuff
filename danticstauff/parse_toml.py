from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

import hvac
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


def get_kv2_secret(
    path: str,
    *,
    mount_point: str = "secret",
    version: Optional[int] = None,
    url: Optional[str] = None,
    token: Optional[str] = None,
    namespace: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Read a HashiCorp Vault KV v2 secret and return the inner data payload.

    Raises:
        RuntimeError: if url/token are missing.
        hvac.exceptions.InvalidPath / Forbidden / VaultError: for Vault issues.
    """
    url = url or os.getenv("VAULT_ADDR")
    token = token or os.getenv("VAULT_TOKEN")
    namespace = namespace or os.getenv("VAULT_NAMESPACE")

    if not url or not token:
        raise RuntimeError(
            "Vault URL and token are required (via args or VAULT_ADDR/VAULT_TOKEN)."
        )

    client = hvac.Client(url=url, token=token, namespace=namespace)

    # Will raise if path/mount is wrong or permission denied
    resp = client.secrets.kv.v2.read_secret_version(
        path=path,
        mount_point=mount_point,
        version=version,  # still supported in hvac; quiets deprecation warnings in older versions
    )
    return resp["data"]["data"]


class VaultSettingsSource(PydanticBaseSettingsSource):
    """
    A custom settings source that loads values from HashiCorp Vault (KV v2).

    It queries a fixed path ("demo" here, adjust as needed) and exposes
    keys as settings fields.
    """

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        try:
            # Adjust `path="demo"` to your app-specific path
            self._secret = {k.lower(): v for k, v in get_kv2_secret(path="demo").items()} or {}
        except Exception:
            # Fall back gracefully if Vault is unavailable
            self._secret = {}

    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        # Return: (value, key_used, value_is_complex)
        field_value,field_name,is_complex =  self._secret.get(field_name), field_name, False
        return field_value,field_name,is_complex

    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,
    ) -> Any:
        # No special preparation needed for strings/numbers
        return value

    def __call__(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        # Iterate over declared model fields and fetch Vault values
        for name, field in self.settings_cls.model_fields.items():
            value, key, is_complex = self.get_field_value(field, name)
            value = self.prepare_field_value(name, field, value, is_complex)
            if value is not None:
                out[key] = value
        return out


class Settings(BaseSettings):
    # .env-style file is supported in v2 via model_config
    model_config = SettingsConfigDict(env_file="app.prod.conf", env_file_encoding="utf-8")

    api_key: str
    app_name: str
    environment: str
    app_version: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,  # present when env_file is set
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Typical order: init kwargs > env vars > .env file > Vault > file secrets
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            VaultSettingsSource(settings_cls),
            file_secret_settings,
        )


if __name__ == "__main__":
    # Instantiate to pull from (in order): kwargs, env, .env, Vault, file secrets
    s = Settings()
    print(s.model_dump())
