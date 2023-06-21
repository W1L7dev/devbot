import json

def visualize_json(data):
    """
    Visualize JSON data

    Args:
        data (int): The data to visualize.

    Returns:
        str: The vizualization of the data.
    """
    def traverse_json(obj, indent=0):
        result = ""
        if isinstance(obj, dict):
            for key, value in obj.items():
                result += f"{' ' * indent}{key}:"
                if isinstance(value, dict) or isinstance(value, list):
                    result += "\n"
                result += traverse_json(value, indent + 2)
        elif isinstance(obj, list):
            for item in obj:
                result += f"{' ' * indent}- "
                result += traverse_json(item, indent)
        else:
            result += f" {obj}\n"
        return result

    json_data = json.loads(data)
    diagram = traverse_json(json_data)
    return diagram
