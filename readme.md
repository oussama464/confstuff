# Dynaconf vs Pydantic Settings — Comparison Recap

A concise, practical guide to choosing between **Dynaconf** and **Pydantic Settings** (`pydantic-settings`, v2) for Python configuration management.

---

## TL;DR

* **Use Pydantic Settings** when you want **strong typing + validation**, tight **FastAPI** synergy, great IDE/autocomplete, and simple 12‑factor style config (env vars, `.env`, Kubernetes secrets dir).
* **Use Dynaconf** when you want **rich layering & environment switching out of the box** (multiple files/formats, per‑env sections, easy overrides) or when **non‑Python users** need to edit config files safely.

---

## When to pick each

### Pydantic Settings — pick it if:

* You need **schema validation** (enums, nested models, custom validators) and type safety.
* You’re building a **FastAPI** / service‑oriented app.
* Your sources are mostly **env vars**, **.env**, and **Kubernetes secrets**.
* You want config that feels like regular **Pydantic models** (clear contracts, IDE help).

### Dynaconf — pick it if:

* You want **declarative, multi‑file, multi‑format** configuration: TOML/YAML/JSON/INI.
* You need **per‑environment blocks** (e.g., `[default]`, `[production]`) and painless switching.
* Multiple roles (data/ops) will edit config files and you prefer **file‑first** over code‑first.
* You want built‑in **layering/override order** across files + env vars with minimal code.

---

## Feature comparison

| Capability                            | Pydantic Settings                    | Dynaconf                                 |
| ------------------------------------- | ------------------------------------ | ---------------------------------------- |
| Type safety & validation              | **Excellent** (first‑class Pydantic) | Basic; add your own (often via Pydantic) |
| Multi‑file layering                   | Custom source or DIY                 | **Built‑in**                             |
| Multiple formats (TOML/YAML/INI/JSON) | Not built‑in                         | **Built‑in**                             |
| Per‑environment sections in one file  | Not built‑in                         | **Built‑in** (`[production]`, etc.)      |
| Env var overrides                     | Yes (nested via `__`)                | Yes (nested via `__`)                    |
| `.env` support                        | Yes                                  | Yes                                      |
| Kubernetes secrets dir                | **Yes** (`secrets_dir`)              | Via files or env vars                    |
| FastAPI integration                   | **Best**                             | Manual (pair with Pydantic)              |
| IDE/autocomplete                      | **Great**                            | Okay (dynamic)                           |

---
