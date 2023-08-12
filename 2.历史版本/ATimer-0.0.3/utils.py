from models import Project
import datetime
import os


# 有问题，待修改


def get_projects():
    projects = []
    # 扫描项目文件夹,加载所有项目
    for filename in os.listdir('projects'):
        if filename.endswith('.md'):
             project = load_project(filename)
             projects.append(project)
    return projects

def load_project(filename):
    name = os.path.splitext(filename)[0]
    project = Project(name)
    # 从文件名对应的md文件加载项目数据
    return project 

def save_project(project):
    filename = f"{project.name}.md"
    # 将项目数据保存到对应的md文件
    pass