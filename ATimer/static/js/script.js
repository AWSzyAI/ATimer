// 获取元素
const newBtn = document.getElementById('new-btn');
const modal = document.getElementById('new-modal');

// 新建按钮点击事件  
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




function showModal() {
    fetch('/new-project-modal')
      .then(res => res.text())
      .then(html => {
        document.body.innerHTML += html;
      })
  }