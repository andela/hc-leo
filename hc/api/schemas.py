check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "timeout": {"type": "number", "minimum": 60, "maximum": 604800},
        "grace": {"type": "number", "minimum": 60, "maximum": 604800},
        "nagging_interval": {"type": "number", "minimum": 60, "maximum": 604800},
        "channels": {"type": "string"}
    }
}
