# 🎼 Maestro

A CLI tool for orchestrating Azure Container Apps.

## Overview

Maestro manages an "orchestra" of Azure Container Apps by maintaining local YAML representations and synchronizing them with Azure. It uses musical terms as commands to make container app management more intuitive and memorable.


## Installation

### From PyPI (when published)
```bash
pip install azure-maestro
```

### From Source
1. Clone this repository:
   ```bash
   git clone https://github.com/dsouflis/maestro.git
   cd maestro
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Make sure Azure CLI is installed and you're logged in:
   ```bash
   az login
   ```

### Prerequisites
- Python 3.11+
- Azure CLI (`az`) installed and configured
- Azure subscription with appropriate permissions for Container Apps

## Usage

### Getting Started

1. **Initialize your orchestra** (`inizio`):
   ```bash
   maestro inizio
   ```
   This creates local state and lets you select an Azure resource group.

2. **Sync with Azure** (`preludio`):
   ```bash
   maestro preludio
   ```
   Downloads existing Container Apps as local YAML files and syncs state. You'll get warnings if an app contains secrets, as the secret values are not downloaded. 
   You must set them with the appropriate command before the local YAML is suitable for deployment.

3. **Make changes locally** using the various commands below.

4. **Deploy changes** (`esecuzione`):
   ```bash
   maestro esecuzione
   ```
   Sends your local modifications to Azure.

### Commands

| Command                                         | Musical Term           | Description |
|-------------------------------------------------|------------------------|-------------|
| `inizio`                                        | Beginning              | Initialize local state, select resource group |
| `preludio`                                      | Prelude                | Sync local state with Azure Container Apps |
| `repertorio aggiungere <file>`                  | Add to repertoire      | Add a local ACA YAML to state |
| `repertorio togliere <app>`                     | Remove from repertoire | Remove an app from local state |
| `crescendo <app> <number>`                      | Crescendo              | Increase app's max replicas |
| `diminuendo <app> <number>`                     | Diminuendo             | Decrease app's max replicas |
| `pianissimo <app> <secret> <value>`             | Very soft              | Set a secret value |
| `valore <app> <container index> <name> <value>` | Value                  | Deploy local changes to Azure |
| `esecuzione`                                    | Performance            | Deploy local changes to Azure |
| `coda`                                          | Ending                 | Delete local state |

### Examples

```bash
# Initialize and sync
maestro inizio
maestro preludio

# Scale up an app
maestro crescendo my-api 5

# Set a secret
maestro pianissimo my-api database-password "my-secure-password"

# Deploy changes
maestro esecuzione

# Clean up
maestro coda
```

## How It Works

1. **Local State**: Maestro maintains a `partitura.json` file (partitura = musical score) that tracks:
   - Selected Azure resource group
   - Container apps and their local YAML files
   - Which apps have been modified locally

2. **YAML Files**: Each Container App is represented as a local YAML file containing the complete app configuration.

3. **Dirty Tracking**: The tool tracks which apps have been modified locally (marked as "dirty") and only updates those during deployment.

4. **Azure Integration**: Uses Azure CLI commands under the hood to interact with Azure Container Apps.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

### Project Structure

- `main.py` - CLI entry point and argument parsing
- `types.py` - Pydantic models and type definitions
- `azure_cli.py` - Azure CLI integration functions
- `state_management.py` - Local state operations
- `commands/` - Command implementations organized by theme
- `partitura.json` - Local state file (created after `inizio`)
- `*.yaml` - Container App configuration files (created after `preludio`)

## Musical Terminology

The command names are inspired by Italian musical terms:

- **Inizio** (Beginning) - Start your orchestration
- **Preludio** (Prelude) - Prepare for the performance
- **Crescendo** (Gradually louder) - Scale up
- **Diminuendo** (Gradually softer) - Scale down  
- **Pianissimo** (Very soft) - Handle secrets quietly
- **Esecuzione** (Performance/Execution) - Deploy your composition
- **Valore** (Note Value) - Set an env var
- **Coda** (Ending) - Conclude and clean up
- **Repertorio** (Repertoire) - Manage your collection

## Contributing

Feel free to submit issues and enhancement requests! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
