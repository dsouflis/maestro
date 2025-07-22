import yaml
import questionary
from azure_cli import list_container_apps
from state_management import local_state_exists, read_local_state, save_local_state, get_state
from models import ContainerApp, ContainerAppEntry

def preludio(args):
    """Synchronize local state with Azure."""
    if not local_state_exists():
        print("𝄋 Local state does not exist. Are you in the correct directory? If you want to initialize local state in this directory, run 'maestro inizio'")
        return
    
    read_local_state()
    state = get_state()
    
    if len([a for a in state.apps.values() if a.is_dirty]) > 0:
        answer = questionary.confirm("𝄋 Locally changed apps exist! Continue and override them?").ask()
        if not answer:
            return
    
    app_list = list_container_apps(state.resource_group)
    apps = [ContainerApp.model_validate(c) for c in app_list]

    state_app_names = set(state.apps.keys())
    read_app_names = set([a.name for a in apps])
    newfound_apps = [a for a in apps if not a.name in state_app_names]
    existing_apps = [a for a in apps if a.name in state_app_names]
    missing_app_names = [n for n in state_app_names if not n in read_app_names]
    missing_app_names_length = len(missing_app_names)

    if missing_app_names_length > 0:
        if missing_app_names_length > 1:
            print(f"𝄋 There are {missing_app_names_length} apps that are not in local state.")
            print("𝄋 Please delete them with:")
            for a in missing_app_names:
                print(f"𝄋   az repertorio togliere {a}")
        else:
            print(f"𝄋 App {missing_app_names[0]} is not in local state.")
            print(f"𝄋 Please delete it with 'az repertorio togliere {missing_app_names[0]}'");

    if len(newfound_apps) > 0:
        print(f"𝄋 There are {len(newfound_apps)} new apps that are not in local state:" + (", ".join([a.name for a in newfound_apps])))
        app_with_valueless_secrets = [a.name for a in newfound_apps 
                                      if a.properties and a.properties.configuration and a.properties.configuration.secrets and len([s for s in a.properties.configuration.secrets if not s.value]) > 0]
        if(len(app_with_valueless_secrets) > 0):
            print(f"𝄋 Caveat: There are {len(app_with_valueless_secrets)} apps with secrets having no value! You will have to add values manually!")
        answer = questionary.confirm("Do you want to add them?").ask()
        if answer:
            for a in newfound_apps:
                if a.properties and a.properties.configuration and a.properties.configuration.secrets:
                    for s in a.properties.configuration.secrets:
                        s.value = 'CHANGE-IT'
                        print(f"𝄋 Use 'maestro pianissimo {a.name} {s.name} {{NEW-VALUE}}'")
                filename = f"{a.name}.yaml"
                a_dict = a.model_dump()
                with open(filename, 'w') as f:
                    yaml.dump(a_dict, f)
                state.apps[a.name] = ContainerAppEntry.model_validate({
                    'filename': filename,
                    'is_dirty': False,
                })
            save_local_state()
            print(f"𝄋 Added {len(app_with_valueless_secrets)} apps and saved them to: " +(", ".join([f'{a.name}.yaml' for a in newfound_apps])))
    
    if len(existing_apps) > 0:
        for a in existing_apps:
            local_app_entry = state.apps[a.name]
            filename = local_app_entry.filename
            with open(filename, 'r') as f:
                app_data = yaml.safe_load(f)
                local_app = ContainerApp.model_validate(app_data)
                if a.properties and a.properties.configuration and a.properties.configuration.secrets:
                    for s in a.properties.configuration.secrets:
                        if local_app.properties and local_app.properties.configuration and local_app.properties.configuration.secrets:
                            old_value_list = [x.value for x in local_app.properties.configuration.secrets if x.name == s.name]
                            if len(old_value_list):
                                s.value = old_value_list[0]
                        if not s.value:    
                            s.value = 'CHANGE-IT'
                            print(f"𝄋 Did not find value in local app. Find the value and use 'maestro pianissimo {a.name} {s.name} {{NEW-VALUE}}'")
                data = a.model_dump()
                with open(filename, 'w') as f:
                    yaml.dump(data, f)
                state.apps[a.name].is_dirty = False
        save_local_state()
        print(f"𝄋 Synchronized {len(existing_apps)} apps")