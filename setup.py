import os
import setuptools
# from setuptools import setup

_version = '0.00.00'
my_dir = os.path.dirname(os.path.realpath(__file__))
my_version_file = my_dir + "/VERSION"
if os.path.exists(my_version_file):
    with open(my_version_file) as fIn:
        _version=fIn.readline().strip()
else:
    pkg_info_files = (my_dir + "/PKG-INFO", my_dir + "/n0struct.egg-info/PKG-INFO")
    for pkg_info_file in pkg_info_files:
        if os.path.exists(pkg_info_file):
            with open(pkg_info_file) as fIn:
                # lines = fIn.readlines()
                # for line in lines:
                    # line = line.strip()
                    # if ": " in line:
                        # line_parts = line.strip().split(": ",1)
                    # else:
                        # raise Exception(str(lines))
                # pkg_info=dict([line.strip().split(": ",1) for line in lines])    
                
                pkg_info=dict([line.strip().split(": ",1) for line in fIn.readlines()])    
                if "Version" in pkg_info:
                    _version = pkg_info.get("Version")
                else:
                    raise Exception("Version is not found in " + pkg_info_file + ":\n" + str(pkg_info))
            break
    else:
        print("Impossible to find and load any of below files: %s" % (str([my_version_file].extend(pkg_info_files))))
print(_version)

# with open("README.md", "rt") as fIn:
    # long_description = fIn.read()

# _packages = setuptools.find_packages()
# _packages.append("aaa")
# _packages = setuptools.find_packages() + ["aaa"]
# print(_packages)

setuptools.setup(
    name = "n0struct",
    version = _version,
    description = "list/OrderedDict extensions allow to work with structure, generated for example by json.loads(..), using xpath approach",
    author = "pythonist552",
    author_email = "pythonist552@gmail.com",
    long_description = "list/OrderedDict extensions allow to work with structure, generated for example by json.loads(..), using xpath approach",
    long_description_content_type="text/markdown",    
    url = "https://github.com/pythonist552/n0struct/",
    license = 'ASL',
    # packages=['n0struct'],
    # packages = ["tests"] + setuptools.find_packages(),
    packages = setuptools.find_packages(),
    platforms = ["any"],
    classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite = "tests",
    python_requires = ">=3.7",
    zip_safe = False
)
