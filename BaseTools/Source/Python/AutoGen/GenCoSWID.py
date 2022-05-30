import configparser
from os import path
import subprocess


class ModuleCoSWID(object):
    '''Create a per-module ini file with SBOM related data

    Also try to get the git HEAD commit hash if the project is
    versioned by git

    '''

    def __init__(self, ModuleAutoGen):
        self.Name = ModuleAutoGen.Name
        self.Guid = ModuleAutoGen.Guid
        self.Version = ModuleAutoGen.Version

        self.colloquial_version = None
        try:
            process = subprocess.run(["git", "rev-parse", "HEAD"],
                                     capture_output=True,
                                     check=True)
            self.colloquial_version = process.stdout.decode("utf-8").strip()
        # If either git is not in the system, the tree is not in a
        # git repo or anything else just don't fail
        except:
            pass

        self.FilePath = path.join(ModuleAutoGen.BuildDir, self.Name + ".ini")

    def Generate(self):
        config = configparser.ConfigParser()

        config["uSWID"] = {
            "tag-id": self.Guid,
            "software-name": self.Name,
            "software-version": self.Version,
        }

        if self.colloquial_version is not None:
            config["uSWID"]["colloquial-version"] = self.colloquial_version

        with open(self.FilePath, 'w') as f:
            config.write(f)
