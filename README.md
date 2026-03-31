<div align="center">

# awspss

**AWS Identity Center Permission Sets Switcher**

[![PyPI version](https://img.shields.io/pypi/v/awspss.svg)](https://pypi.org/project/awspss/)
[![Python](https://img.shields.io/pypi/pyversions/awspss.svg)](https://pypi.org/project/awspss/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Interactively select an AWS Account and Permission Set after SSO login,
and the temporary credentials are automatically set in your current shell.

[English](#installation) | [한국어](docs/README.ko.md)

<img src="docs/demo.svg" alt="awspss demo" width="620">

</div>

---

## Features

- **Browser-based SSO Login** — OIDC device authorization with token caching
- **Interactive Selection** — fzf-style fuzzy search for Account and Permission Set
- **Quick Switch** — `awspss sw RoleName` to skip interactive selection
- **Tab Completion** — `awspss sw <Tab>` to autocomplete permission sets
- **Shell Integration** — credentials are set directly in your current shell (no `--profile` needed)
- **Credential Expiry** — shows when your temporary credentials expire
- **Identity Check** — `awspss whoami` to verify current credentials

## Installation

### pip / pipx

```bash
pip install awspss

# or pipx (recommended for CLI tools)
pipx install awspss
```

### Homebrew

```bash
brew tap boseung-code/tap
brew install awspss
```

### From source

```bash
git clone https://github.com/boseung-code/awspss.git
cd awspss
pip install -e .
```

## Quick Start

```bash
# 1. Register shell function + tab completion
eval "$(awspss init)"

# 2. Configure SSO connection
awspss configure

# 3. Login and select account/permission set
awspss login

# 4. Switch to another account/permission set
awspss sw

# 5. Quick switch (permission set only, tab completion supported)
awspss sw AdministratorAccess
```

## Setup

### 1. Register shell function

Shell function registration is required for `awspss login` and `awspss sw` to set credentials directly in your current shell. This also enables Tab completion.

```bash
eval "$(awspss init)"
```

This will:
1. Detect your shell rc file (`.bashrc` or `.zshrc`)
2. Ask for confirmation
3. Register to rc file + activate immediately in current shell

Duplicate registration is prevented. New terminals will activate automatically.

To register manually, add to your `.bashrc` or `.zshrc`:

```bash
eval "$(awspss init --print)"
```

### 2. Configure SSO connection

```bash
awspss configure
```

Prompts for start-url and region interactively. You can also pass them directly:

```bash
awspss configure --start-url https://your-org.awsapps.com/start --region ap-northeast-2
```

## Usage

### Login

```bash
awspss login
```

Always performs a fresh SSO authentication via browser. After authentication, select Account → Permission Set and credentials are set in your current shell.

### Switch credentials

```bash
awspss sw
```

Switch to a different Account/Permission Set using cached token (no re-login). Automatically re-authenticates if the token has expired.

### Quick switch (permission set only)

```bash
awspss sw AdministratorAccess
```

Switch to a different Permission Set within the same account without interactive selection. Tab completion is supported — press `Tab` after `awspss sw ` to see available permission sets.

### Check current identity

```bash
awspss whoami
```

### Clear credentials

```bash
awspss unset
```

### Logout (clear cached token)

```bash
awspss logout
```

### Without shell function (eval)

```bash
eval "$(awspss login)"
eval "$(awspss sw)"
```

## Commands

| Command | Description |
|---|---|
| `awspss init` | Register shell function + tab completion |
| `awspss configure` | Configure SSO connection |
| `awspss login` | SSO login (always re-authenticates) |
| `awspss sw` | Switch account/permission set |
| `awspss sw [ROLE]` | Quick switch permission set (Tab completion) |
| `awspss whoami` | Show current AWS identity |
| `awspss unset` | Clear AWS credentials from current shell |
| `awspss logout` | Clear cached SSO token |
| `awspss --version` | Show version |

## Configuration

| Method | Example |
|---|---|
| Config file | `~/.awspss/config.json` (via `awspss configure`) |
| Environment variable | `AWSPSS_START_URL`, `AWSPSS_REGION` |
| CLI flag | `--start-url`, `--region` |

Priority: CLI flag > Environment variable > Config file

## Requirements

- Python 3.10+
- AWS Identity Center (SSO) enabled
- A browser for SSO authentication

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

<div align="center">

If you find this tool useful, please consider giving it a star!

</div>
