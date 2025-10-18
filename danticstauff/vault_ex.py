import os
import hvac
from typing import Any, Dict, Optional

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
    Read a HashiCorp Vault KV v2 secret.

    Args:
        path: Secret path relative to the KV mount (e.g. "app/prod/api").
        mount_point: KV v2 mount point name (default: "secret").
        version: Optional specific version to read.
        url: Vault address. Falls back to $VAULT_ADDR if not provided.
        token: Vault token. Falls back to $VAULT_TOKEN if not provided.
        namespace: Vault namespace (HCP/Enterprise). Falls back to $VAULT_NAMESPACE.

    Returns:
        The secret data dict (the inner 'data' payload).

    Raises:
        hvac.exceptions.InvalidPath: if the secret/path doesn’t exist.
        hvac.exceptions.Forbidden: if access is denied.
        hvac.exceptions.VaultError: for other Vault-related errors.
        RuntimeError: if url/token are missing.
    """
    url = url or os.getenv("VAULT_ADDR")
    token = token or os.getenv("VAULT_TOKEN")
    namespace = namespace or os.getenv("VAULT_NAMESPACE")

    if not url or not token:
        raise RuntimeError("Vault URL and token are required (via args or VAULT_ADDR/VAULT_TOKEN).")

    client = hvac.Client(url=url, token=token, namespace=namespace)

    # Will raise if path/mount is wrong or permission denied
    resp = client.secrets.kv.v2.read_secret_version(
        path=path,
        mount_point=mount_point,
        version=version,  # 👈 quell the deprecation warning
    )
    return resp["data"]["data"]

    # KV v2 structure: {'data': {'data': {...}, 'metadata': {...}}, 'wrap_info': None, ...}

if __name__ == "__main__":
    secret = get_kv2_secret("demo", mount_point="secret", version=None)
    print(secret)