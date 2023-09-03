
function formatDateTime(dateTime) {
  // 格式化为 YYYY-MM-DD HH:MM:SS 格式
  let year = dateTime.getFullYear();
  let month = (dateTime.getMonth() + 1).toString().padStart(2, '0');
  let day = dateTime.getDate().toString().padStart(2, '0');
  let hours = dateTime.getHours().toString().padStart(2, '0');
  let minutes = dateTime.getMinutes().toString().padStart(2, '0');
  let seconds = dateTime.getSeconds().toString().padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function createRecord(record) {
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/create-record');
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log('Record created:', record);
    } else {
      console.error('Failed to create record:', xhr.status);
    }
  }
  
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(record));
}



// 格式化时间
function formatDateTime(dateTime) {
  let date = new Date(dateTime);
  let formatted = date.getFullYear() + '-'
    + (date.getMonth() + 1) + '-'
    + date.getDate() + ' '
    + date.getHours() + ':'
    + date.getMinutes() + ':'
    + date.getSeconds();

  return formatted; 
}




// 获取所有按钮
const timerBtns = document.querySelectorAll('.timer-btn');

// 为每个按钮绑定点击处理
timerBtns.forEach(btn => {

  let active = false;
  let startTime, endTime;

  const clickHandler = function() {

    if(!active) {
      // 开始录制
      startTime = new Date(); 

      active = true;
      btn.textContent = 'Stop';

    } else {
      // 停止录制
      endTime = new Date();

      active = false;
      btn.textContent = 'Record';

      let record = {
        project_id: btn.id,
        start_time: formatDateTime(startTime),
        end_time: formatDateTime(endTime)
      };

      createRecord(record);
    }

  };

  btn.addEventListener('click', clickHandler);

});