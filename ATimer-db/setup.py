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
        'werkzeug'
    ],

    entry_points={
        'console_scripts': [
            'atimer = ATimer.manage:cli'
        ]
    },

    # 包数据
    package_data={
        'ATimer': [
            'schema.sql',
            'static/css/*',
            'static/js/*',
            'templates/*',
            'templates/auth/*',
            'templates/base.html'
        ]
    },

    # metadata
    author='Ziyan Shi',
    author_email='szy@nnu.edu.cn',
    description='A project tracker app',
    url='https://github.com/AWSzyAI/ATimer'  
)