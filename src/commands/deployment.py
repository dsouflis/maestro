from azure_cli import update_container_app
from state_management import local_state_exists, read_local_state, save_local_state, get_state

def esecuzione(args):
    """Deploy local changes to Azure."""
    if not local_state_exists():
        print("𝄆 Local state does not exist. Are you in the correct directory?")
        return
    
    read_local_state()
    state = get_state()
    changed = False
    
    for app_name in state.apps.keys():
        if app_name != 'nginx': 
            continue  # testing
        
        app_entry = state.apps[app_name]
        if app_entry.is_dirty:
            result = update_container_app(app_name, state.resource_group, app_entry.filename)
            if result:
                app_entry.is_dirty = False
                changed = True
                print(f"𝄆 App {app_name} was updated")
    
    if changed:         
        save_local_state()