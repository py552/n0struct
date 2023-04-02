import os
import setuptools

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
                pkg_info=dict([line.strip().split(": ",1) for line in fIn.readlines()])    
                if "Version" in pkg_info:
                    _version = pkg_info.get("Version")
                else:
                    raise ModuleNotFoundError("Version is not found in " + pkg_info_file + ":\n" + str(pkg_info))
            break
    else:
        full_list_of_dirs_where_we_search = [my_version_file]
        full_list_of_dirs_where_we_search.extend(pkg_info_files)
        print("Impossible to find and load any of below files: %s" % (str(full_list_of_dirs_where_we_search)))
print(_version)

with open("requirements.txt", "rt") as fIn:
    reqs = fIn.readlines()

setuptools.setup(
    name = "n0struct",
    version = _version,
    description = "list/dict extensions allow to load/save/serialize/deserialize xml/json/csv/dsv/fwf files into python/from structures, compare them and work with them using xpath approach",
    author = "pythonist552",
    author_email = "pythonist552@gmail.com",
    long_description = "list/dict extensions allow to load/save/serialize/deserialize xml/json/csv/dsv/fwf files into/from python structures, compare them and work with them using xpath approach",
    long_description_content_type="text/markdown",    
    url = "https://github.com/pythonist552/n0struct/",
    license = 'ASL',
    packages = setuptools.find_packages(),
    platforms = ["any"],
    classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    test_suite = "tests",
    python_requires = ">=3.7",
    install_requires = reqs,
    zip_safe = False,
)
