import configparser
import os.path as path
import subprocess

# TODO: This is kind of inspired from GenMake module although is very incomplete
#
# Over there they use things like templates for generating files and
# SaveOnChange for saving file's content plus a lot more of nice
# things. This is just a start.
#
# TODO: Is the name *CoSWID precise?
#
# TODO: Does is make sense to have something else than ModuleCoSWID?
#
# In GenMake there are, the top level class: BuildFile and then
# ModuleMakefile, CustomMakefile (not sure what this is),
# PlatformMakefile and TopLevelMakefile
#
# Maybe TopLevelCoSWID could be interesenting, don't know where the
# TopLevelMakefile ends up being
class ModuleCoSWID(object):
    def __init__(self, ModuleAutoGen):
        self.Name = ModuleAutoGen.Name
        self.Guid = ModuleAutoGen.Guid
        self.Version = ModuleAutoGen.Version

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

        if not self.colloquial_version is None:
            config["uSWID"]["colloquial-version"] = self.colloquial_version

        with open(self.FilePath, 'w') as f:
            config.write(f)

