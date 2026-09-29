def edit_file(file_path, old, new):
    with open(file_path, "r") as f:
        content = f.read()

    if old not in content:
        return {
            "success": False,
            "message": "Target code not found"
        }

    content = content.replace(old, new)

    with open(file_path, "w") as f:
        f.write(content)

    return {
        "success": True,
        "message": "File updated"
    }