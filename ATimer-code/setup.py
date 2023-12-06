from setuptools import find_packages, setup

setup(
    name='ATimer', 
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    # 依赖
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'click',
        'python-dotenv',
        'setuptools',
        'werkzeug',
        'flask-login',
        'flask_migrate'
    ],
    
    # metadata
    author='Ziyan Shi',
    author_email='szy@nnu.edu.cn',
    description='A project tracker app',
    url='https://github.com/AWSzyAI/ATimer'  
)
