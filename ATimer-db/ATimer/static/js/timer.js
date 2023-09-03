let timerBtn = document.getElementById('timer-btn');
let isactive = 'inactive';
let startTime = null;

timerBtn.addEventListener('click', function() {
  if (isactive === 'inactive') {
    // Start timer
    startTime = new Date();
    isactive = 'active';
    timerBtn.innerText = 'Stop';
  } else {
    // Stop timer
    isactive = 'inactive';
    timerBtn.innerText = 'Record';
    let endTime = new Date();
    let record = {
      start_time: formatDateTime(startTime),
      end_time: formatDateTime(endTime)
    };
    createRecord(record);
    startTime = null;
  }
});

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
  xhr.open('POST', '/create_record');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Record created successfully
        console.log('Record created:', record);
      } else {
        console.error('Failed to create record:', xhr.status);
      }
    }
  };
  xhr.send(JSON.stringify(record));
}