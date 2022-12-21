from setuptools import find_packages,setup
# /config/workspace/requirements.txt

from typing import List

REQUIREMENTS_FILENAME="requirements.txt"
HYPHEN_E_DOT= "-e ."


def get_requirements()->List[str]:
    with open(REQUIREMENTS_FILENAME) as requirement_Packages :
        requirement_Packages=requirement_Packages.readlines()
    requirement_list=[requirement_name.replace("/n","") for requirement_name in requirement_Packages]
    

    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

setup(
    name="Sensor",
    version="0.0.1",
    author="ineuron",
    author_email="prashant886882@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)

