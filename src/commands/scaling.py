import yaml
from pathlib import Path
from state_management import local_state_exists, read_local_state, save_local_state, get_state
from models import ContainerApp

def dinamica(symbol, num, args):
    """Common function for scaling operations."""
    if not local_state_exists():
        print(f"{symbol} Local state does not exist. Are you in the correct directory?")
        return
    
    read_local_state()
    state = get_state()
    
    if not args.app_name in state.apps.keys():
        print(f"{symbol} App {args.app_name} does not exist")
        return
    
    app_entry = state.apps[args.app_name]
    file_path = Path(app_entry.filename)
    path_exists = file_path.exists()
    if not path_exists:
        print(f"{symbol} ERROR: File {app_entry.filename} does not exist!")
        return
    
    with open(app_entry.filename, 'r') as f:
        app_data = yaml.safe_load(f)
        app = ContainerApp.model_validate(app_data)
        app.properties.template.scale.maxReplicas += num
        app_entry.is_dirty = True
    
    if not app_entry.is_dirty:
        print(f"{symbol} App {args.app_name} not changed")
    else:
        print(f"{symbol} Done. You can now do 'maestro esecuzione' to send local state to Azure")
        data = app.model_dump()
        with open(app_entry.filename, 'w') as f:
            yaml.dump(data, f)
        save_local_state()

def crescendo(args):
    """Increase app scaling."""
    dinamica('𝆒', args.incr, args)

def diminuendo(args):
    """Decrease app scaling."""
    dinamica('𝆓', -args.decr, args)