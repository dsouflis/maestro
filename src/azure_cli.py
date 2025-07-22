import subprocess
import json
from typing import List, Any, Optional

def az(*args: List[str]) -> Optional[Any]:
    """Execute Azure CLI command and return parsed JSON result."""
    params = [r"c:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd", *args]
    result = subprocess.run(params, capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        return None

def check_login() -> Optional[dict]:
    """Check if user is logged into Azure CLI."""
    return az("account", "show")

def list_resource_groups() -> Optional[List[str]]:
    """Get list of available resource groups."""
    return az("group", "list", "--query", "[].name")

def list_container_apps(resource_group: str) -> Optional[List[dict]]:
    """Get list of container apps in the specified resource group."""
    return az("containerapp", "list", "--resource-group", resource_group)

def update_container_app(app_name: str, resource_group: str, yaml_file: str) -> Optional[dict]:
    """Update a container app using a YAML file."""
    return az("containerapp", "update", "--name", app_name, "--resource-group", resource_group, "--yaml", yaml_file)