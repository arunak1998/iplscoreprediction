from setuptools import find_packages,setup
from typing import List


HYPEN_E_DOT='-e .'
def get_requirement(file_path:str)->List[str]:
    requirement=[]
    with open(file_path) as filr_obj:
        requirement=filr_obj.readlines()
        requirement=[req.replace("\n","") for req in requirement]
        if HYPEN_E_DOT in requirement:
            requirement.remove(HYPEN_E_DOT)
    return requirement


    



setup(
name='iplproject',
version='0.0.1',
author='Arun',
author_email='aktooall@gamil.com',
packages=find_packages(),
install_requires=get_requirement('requirements.txt')
)