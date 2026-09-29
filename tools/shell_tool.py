import subprocess

def run_command(command):
    if command.startswith("pip install"):
        command += " -i https://pypi.tuna.tsinghua.edu.cn/simple"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }