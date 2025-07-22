import json
from pathlib import Path
from typing import Optional
from models import Partitura

# Global state variable
state: Optional[Partitura] = None

def read_local_state() -> None:
    """Read local state from partitura.json file."""
    global state
    with open('partitura.json', 'r') as f:
        contents = json.load(f)
        state = Partitura.model_validate(contents)

def save_local_state() -> None:
    """Save current state to partitura.json file."""
    global state
    if not state:
        print('In-memory state is null')
        return
    json_state = state.model_dump()
    with open('partitura.json', 'w') as f:
        json.dump(json_state, f, indent=2)

def local_state_exists() -> bool:
    """Check if local state file exists."""
    file_path = Path('partitura.json')
    return file_path.exists()

def get_state() -> Optional[Partitura]:
    """Get the current global state."""
    return state

def set_state(new_state: Partitura) -> None:
    """Set the global state."""
    global state
    state = new_state
