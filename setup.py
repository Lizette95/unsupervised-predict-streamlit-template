from setuptools import setup, find_packages

setup(
    name = 'unsupervised_functions',
    version = '0.1',
    packages = find_packages(exclude=['tests*']),
    license = 'MIT',
    description = 'Movie Recommender helper functions',
    long_description = open('README.md').read(),
    install_requires = ['numpy', 'pandas', 'seaborn', 'random', 'cufflinks', 'sklearn', 'plotly.offline', 'scikit-surprise'],
    url = 'https://github.com/Lizette95/unsupervised-predict-streamlit-template',
    author = 'JHB_Team_RM4',
    author_email = ['bulelaninkosi9@gmail.com'] # add emails
    
)