# my_own_namespace.yandex_cloud_elk

Ansible collection with the `my_own_module` module and a single-task role
that creates a text file on the target host.

## Contents

- module `my_own_namespace.yandex_cloud_elk.my_own_module` — creates/updates
  a text file at `path` with `content`, idempotent, supports check mode.
- role `my_own_namespace.yandex_cloud_elk.my_own_module` — wraps the module
  in one task, all module parameters have defaults.

## Requirements

- ansible-core >= 2.9

## Role variables (defaults)

| Variable                | Default                 | Description                  |
|-------------------------|-------------------------|------------------------------|
| `my_own_module_path`    | `/tmp/ansible_demo.txt` | Path to the file to manage   |
| `my_own_module_content` | `"hello world\n"`       | Content to write to the file |

## Usage

```yaml
- hosts: localhost
  connection: local
  roles:
    - my_own_namespace.yandex_cloud_elk.my_own_module