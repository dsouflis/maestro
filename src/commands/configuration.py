import yaml
from pathlib import Path
from state_management import local_state_exists, read_local_state, save_local_state, get_state
from models import ContainerApp

def pianissimo(args):
    """Set a secret value for an app."""
    if not local_state_exists():
        print("𝆏𝆏 Local state does not exist. Are you in the correct directory?")
        return
    
    read_local_state()
    state = get_state()
    
    if not args.app_name in state.apps.keys():
        print(f"𝆏𝆏 App {args.app_name} does not exist")
        return
    
    app_entry = state.apps[args.app_name]
    file_path = Path(app_entry.filename)
    path_exists = file_path.exists()
    if not path_exists:
        print(f"𝆏𝆏 ERROR: File {app_entry.filename} does not exist!")
        return
    
    with open(app_entry.filename, 'r') as f:
        app_data = yaml.safe_load(f)
        app = ContainerApp.model_validate(app_data)
        if not app.properties or not app.properties.configuration or not app.properties.configuration.secrets:
            print(f"𝆏𝆏 App {app.name} does not have any secrets. Adding secrets is not currently implemented")
            return
        
        for s in app.properties.configuration.secrets:
            if s.name == args.secret_name:
                s.value = args.value
                app_entry.is_dirty = True
    
    if not app_entry.is_dirty:
        print(f"𝆏𝆏 Secret {args.secret_name} not found")
    else:
        print("𝆏𝆏 Done. You can now do 'maestro esecuzione' to send local state to Azure")
        data = app.model_dump()
        with open(app_entry.filename, 'w') as f:
            yaml.dump(data, f)
        save_local_state()