import os
import markdown
import yaml
from flask import Flask, request, jsonify,Blueprint
import uuid
from flask import render_template



app = Flask(__name__)

PROJECTS_DIR = './data'





@app.route('/')
def homepage():
    return render_template('homepage.html')








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

#生成项目ID,保证每个项目唯一标识
def generate_id(): 
  return str(uuid.uuid4())

# 新加入的首页路由
@app.route('/')
def home():
  projects = get_projects()
  return render_template('templates/home.html',projects=projects)




# 增
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    name = data['name']
    status = data['status'] or 'In Planning' # 默认状态为 In Planning
    note = data['note'] or '' # 默认描述为空
    stats = data['stats'] or {} # 默认统计信息为空
    
    filename = f'{name}.md' # 项目文件名
    project_file = f'{PROJECTS_DIR}/{status}/{filename}' # 项目文件路径
    
    # 在对应目录下创建项目文件
    open(project_file, 'w').close()
    
    return jsonify({'message': 'Project created'},201)


@app.route('/new-project')
def new_project():
  return render_template('new_project.html')




# 读取单个项目文件
def load_project(project_file): 
    with open(project_file) as f:
        content = f.read()

    metadata, content = content.split('\n---\n')
    data = yaml.load(metadata,Loader=yaml.FullLoader)

    data['content'] = content

    return data


# 读取所有项目文件
@app.route('/api/projects', methods=['GET'])
def get_projects():
    # 返回项目列表
    # 创建新项目
    projects = []
    for status in ['In Planning', 'In Process', 'Done']:
        status_dir = f'{PROJECTS_DIR}/{status}'
        for filename in os.listdir(status_dir):
            project_file = f'{status_dir}/{filename}'
            project = load_project(project_file)
            projects.append(project)

    return jsonify(projects)

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    # 返回项目列表
    # 创建新项目
    projects = []
    for status in ['In Planning', 'In Process', 'Done']:
        status_dir = f'{PROJECTS_DIR}/{status}'
        for filename in os.listdir(status_dir):
            project_file = f'{status_dir}/{filename}'
            project = load_project(project_file)
            projects.append(project)
    for project in projects:
        if project['id'] == project_id:
            return jsonify(project)
    return jsonify({'message': 'Project not found'}), 404


@app.route('/projects/<project_id>')
def show_project(project_id):
  project = get_project(project_id)
  return render_template('project.html', project=project)


if __name__ == '__main__':
    app.run()