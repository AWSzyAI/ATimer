

// 新建按钮点击事件  
const newBtn = document.getElementById('new-btn');
const modal = document.getElementById('modal');
newBtn.addEventListener('click', () => {
  modal.style.display = 'block';
})




// 取消按钮点击事件
const cancelBtn = document.getElementById('cancel-btn');
cancelBtn.addEventListener('click', () => {
  modal.style.display = 'none'; 
})


// 确定按钮点击事件
const okBtn = document.getElementById('ok-btn');
okBtn.addEventListener('click', () => {

  const name = document.getElementById('project-name').value;
  const status = document.getElementById('project-status').value;

  fetch('/api/projects', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name,
      status
    })
  }).then(res => {
    modal.style.display = 'none';
    window.location.reload();
  })

})

// 获取输入名称 和 选择的状态
const name = document.getElementById('project-name').value;
const status = document.getElementById('project-status').value;

// 提交数据
fetch('/api/projects', {
  method: 'POST',
  body: JSON.stringify({name, status}) 
});


function showModal() {
    fetch('/new-project-modal')
      .then(res => res.text())
      .then(html => {
        document.body.innerHTML += html;
      })
  }