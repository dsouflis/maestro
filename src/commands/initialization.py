import json
import questionary
from pathlib import Path
from azure_cli import list_resource_groups
from state_management import local_state_exists

def inizio(args):
    """Initialize local state by selecting resource group."""
    if local_state_exists():
        print("𝄊 Local state already exists. If you want to erase it, run 'maestro coda'")
        return
    
    resource_groups = list_resource_groups()
    if not resource_groups:
        print("𝄊 No resource groups found")
        return
    
    resource_group = resource_groups[0]
    if len(resource_groups) > 1:
        resource_group = questionary.select(
            "𝄊 Choose a resource group:",
            choices=resource_groups,
        ).ask()
    
    initial_state = {
        'resource_group': resource_group,
        'apps': {},
    }
    
    with open('partitura.json', 'w') as f:
        json.dump(initial_state, f, indent=2)
    
    print("𝄊 Local state created. Please add local ACA YAML files with 'maestro repertorio aggiungere {path to YAML}'")

def coda(args):
    """Delete local state."""
    file_path = Path('partitura.json')
    path_exists = file_path.exists()
    if not path_exists:
        print("𝄌 Local state does not exist. Are you in the correct directory?")
        return
    
    answer = questionary.confirm("𝄌 Do you want to continue?").ask()
    if answer:
        file_path.unlink()    
        print('𝄌 Local state erased')