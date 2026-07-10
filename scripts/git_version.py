import subprocess
Import("env")
try:
    ret = subprocess.check_output(
        ["git", "describe", "--tags", "--always", "--dirty"],
        stderr=subprocess.DEVNULL
    ).decode().strip()
except Exception:
    ret = "unknown"
env.Append(CPPDEFINES=[("GIT_VERSION", env.StringifyMacro(ret))])
