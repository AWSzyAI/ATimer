// static/script.js

function toggleStatus(id) {

    // 获取当前项目的状态
    let projectStatus = document.getElementById(id).dataset.status;
  
    // 切换状态
    let newStatus;
    if(projectStatus === '进行中') {
      newStatus = '暂停';
    } else {
      newStatus = '进行中'; 
    }
  
    // 调用接口修改状态
    fetch(`/project/${id}/status`, {
      method: 'PUT', 
      body: {status: newStatus}
    })
    .then(response => {
      // 更新页面
    });
  
  }



//all.html
function toggleTimer(projectId) {

  let button = document.getElementById('timer-'+projectId);

  if (button.innerText === '开始计时') {
    button.innerText = '停止计时';
    button.dataset.status = 'in progress';

  } else {
    button.innerText = '开始计时'; 
    button.dataset.status = 'paused';
  }

}