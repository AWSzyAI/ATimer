import os
import markdown
import yaml
from flask import Flask, request, jsonify,Blueprint
import uuid
from flask import render_template

# app = Flask(__name__)
app = Flask(__name__)

PROJECTS_DIR = './data'

# 首页路由
@app.route('/')
def home():
  # projects = get_projects()
  # return render_template('templates/home.html',projects=projects)
  return render_template('home.html')

# 项目路由
class Project:
    def __init__(self, name, status,note,stats):
        """
        name: 项目名称
        status: 项目状态: In Planning, In Process, Done, Pause
        note: 项目描述
        stats[daily,weekly,monthly,yearly]: 项目统计信息
        """
        self.name = name
        self.status = status
        self.note = note
        self.stats = stats
    def getName(self):
        return self.name
    def getStatus(self):
        return self.status
    def getNote(self):
        return self.note
    def getStats(self):
        return self.stats
    def setName(self,name):
        self.name = name
    def setStatus(self,status):
        self.status = status
    def setNote(self,note):
        self.note = note
    def setStats(self,stats):
        self.stats = stats



# 增
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_data()
    project_name = request.form.get('name')
    project_status = request.form.get('status') or 'In Planning' # 默认状态为 In Planning
    note = data['note'] or '' # 默认描述为空
    stats = data['stats'] or {} # 默认统计信息为空
    newProject = Project(project_name,project_status,note,stats)
    
    filename = f'{newProject.getName()}.md' # 项目文件名
    project_file = f'{PROJECTS_DIR}/{newProject.getStatus()}/{filename}' # 项目文件路径
    
    # 在对应目录下创建项目文件
    open(project_file, 'w').close()
    
    return jsonify({'message': 'Project created'},201)

#生成项目ID,保证每个项目唯一标识
def generate_id(): 
  return str(uuid.uuid4())



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)