import os
import typing
# Used by class Git():
import subprocess
import signal
from .n0struct_logging import (
    n0print,
    n0debug,
    n0debug_calc,
    n0error,
)
# ******************************************************************************
# ******************************************************************************
class Git():
    _repository_name = None
    _repository_path = None
    _show_result = None
    # ##############################################################################################
    def __init__(self, repo_root_dir: str, repository_url: str, rsa_key_path: str = "", show_result = False):
        self._show_result = show_result
        
        if not repository_url.startswith("ssh://") or not repository_url.endswith(".git"):
            raise SyntaxError("repository_url must be 'ssh://...git'")

        outs = errs = None
        self._repository_path = os.path.abspath(repo_root_dir)
        if not os.path.exists(os.path.join(self._repository_path, ".git")):
            outs, errs = self.run(
                                ["clone", repository_url] +
                                ["--config", "core.sshCommand=ssh -i " + rsa_key_path + " -F /dev/null"] if rsa_key_path else []
                                , show_result
            )
            self._repository_name = repository_url.split("/")[-1].split(".git")[0]
            self._repository_path = os.path.join(self._repository_path, self._repository_name)
        else:
            self._repository_name = os.path.split(self._repository_path)[1]
            if self._show_result:
                n0print(f"Other repository '{self._repository_name}' is already existed")

        if errs and "already exists and is not an empty directory." in errs:
            outs, errs = self.run("pull")
            if outs != "Already up to date.\n":
                if self._show_result:
                    n0debug_calc(outs.strip(), "outs")
                    n0debug_calc(errs.strip(), "errs")
    # ##############################################################################################
    def run(self, git_arguments: typing.Union[str, list], show_result = None) -> tuple:
        if isinstance(git_arguments, str):
            git_arguments = git_arguments.split(" ")
        if show_result or (show_result is None and self._show_result):
            n0print(f"*** git {' '.join(git_arguments)}")
        command_line = ["git",] + git_arguments  # removed walrus operator for compatibility with 3.7
        p = subprocess.Popen(   command_line,
                                cwd = self._repository_path,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True,
                                encoding = "utf-8",
        )
        try:
            timeout_sec = 600  # removed walrus operator for compatibility with 3.7
            outs, errs = p.communicate(timeout = timeout_sec)
        except subprocess.TimeoutExpired:
            raise TimeoutError(
                f"Timeout {timeout_sec} seconds were happened during execution:\n" +
                f"{self._repository_path}>{' '.join(command_line)}"
            )

        if show_result or (show_result is None and self._show_result):
            n0debug_calc(outs.strip(), "outs")
            n0debug_calc(errs.strip(), "errs")
        return outs, errs
    # ##############################################################################################
    def checkout(self, branch_name: str, show_result = None):
        outs, errs = self.run(["checkout", branch_name], show_result)
        return outs, errs
    # ##############################################################################################
    def log(self, git_arguments: typing.Union[str, list]):
        if isinstance(git_arguments, str):
            git_arguments = git_arguments.split(" ")

        outs, errs = self.run(["log",  "--date=format:%y%m%d_%H%M%S", "--pretty=format:%H=%ad=%cn=%s"] + git_arguments, show_result)
        return outs, errs
    # ##############################################################################################
# ******************************************************************************
# ******************************************************************************
