'''

Setup.py is the essential part of packaging and disturbing the python Projects.It is used by Setuptools to define configuration of the Project such as metadata,dependencies,and more 

'''


from setuptools import find_packages,setup 
from typing import List 


def get_requirements()->List[str]:
    """
      This function will return the list of Requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            ## Read lines from the file 
            lines=file.readlines()
            ## Process Each line 
            for line in lines:
                requirement=line.strip()
                ## ignore the Empty lines and -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('requirment.txt file not found')

    return requirement_lst


setup(
    name='NETWORK_SECURITY',
    version='0.0.1',
    author='Valli Raja Sekar',
    author_email='sekarvalliraja@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)


