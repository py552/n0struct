import os
import typing
# Used by class Git():
import subprocess
import signal
# from .n0struct_logging import *
# ******************************************************************************
# ******************************************************************************
class Git():
    _repository_name = None
    _repository_path = None
    # ##############################################################################################
    def __init__(self, repo_root_dir: str, repository_url: str, rsa_key_path: str = ""):
        if not repository_url.startswith("ssh://") or not repository_url.endswith(".git"):
            raise SyntaxError("repository_url must be 'ssh://...git'")

        outs = errs = None
        self._repository_path = os.path.abspath(repo_root_dir)
        if not os.path.exists(os.path.join(self._repository_path, ".git")):
            outs, errs = self.run(
                                ["clone", repository_url] +
                                ["--config", "core.sshCommand=ssh -i " + rsa_key_path + " -F /dev/null"] if rsa_key_path else []
            )
            self._repository_name = repository_url.split("/")[-1].split(".git")[0]
            self._repository_path = os.path.join(self._repository_path, self._repository_name)
        else:
            self._repository_name = os.path.split(self._repository_path)[1]
            n0print("Other repository '%s' is already existed" % self._repository_name)

        if errs and "already exists and is not an empty directory." in errs:
            outs, errs = self.run("pull")
            if outs != "Already up to date.\n":
                n0debug_calc(outs.strip(), "outs")
                n0debug_calc(errs.strip(), "errs")
    # ##############################################################################################
    def run(self, git_arguments: typing.Union[str, list], show_result = True) -> tuple:
        if isinstance(git_arguments, str):
            git_arguments = git_arguments.split(" ")
        n0print("*** git %s" % " ".join(git_arguments))
        # p = subprocess.Popen(   (command_line:=["git",] + git_arguments), # Only for 3.8+
        command_line = ["git",]
        p = subprocess.Popen(   (command_line + git_arguments),
                                cwd = self._repository_path,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True,
                                encoding = "utf-8",
        )
        try:
            # Only for 3.8+: outs, errs = p.communicate(timeout=(timeout_sec:=600)) 
            timeout_sec = 600
            outs, errs = p.communicate(timeout = timeout_sec)
        except subprocess.TimeoutExpired:
            raise TimeoutError("Timeout %d seconds were happened during execution:\n%s>%s" % (timeout_sec, self._repository_path, " ".join(command_line)))

        if show_result:
            n0debug_calc(outs.strip(), "outs")
            n0debug_calc(errs.strip(), "errs")
        return outs, errs
    # ##############################################################################################
    def checkout(self, branch_name: str):
        outs, errs = self.run(["checkout", branch_name])
        return outs, errs
    # ##############################################################################################
    def log(self, git_arguments: typing.Union[str, list]):
        if isinstance(git_arguments, str):
            git_arguments = git_arguments.split(" ")

        outs, errs = self.run(["log",  "--date=format:%y%m%d_%H%M%S", "--pretty=format:%H=%ad=%cn=%s"] + git_arguments)
        return outs, errs
    # ##############################################################################################
# ******************************************************************************
# ******************************************************************************
