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

// static/script.js
/*
let timerBtn = document.getElementsByClassName('timer-btn');
let active = true;
let startTime = null;
let projectId = timerBtn.getAttribute('project-id');

timerBtn.addEventListener('click', function() {
  if (active) {
    // Start timer
    startTime = new Date();
    print(startTime);
    active = false;
    timerBtn.innerText = 'Stop';
  } else {
    // Stop timer
    let endTime = new Date();
    print(endTime);
    active = true;
    timerBtn.innerText = 'Record';
    
    let record = {
      project_id: projectId,
      start_time: formatDateTime(startTime),
      end_time: formatDateTime(endTime),
      time : startTime
    };
    createRecord(record);
    startTime = null;
    console.log('Button clicked for project with ID:', projectId);
  }
});

*/

/*
function clickHandler(e) {
  let btn = e.target;
  let projectId = btn.id;
  let active = false;
  let startTime, endTime;
  if(!active){
    startTime = new Date();
    active = true;
    btn.innerText = 'Stop';
  }else{
    endTime = new Date();
    active = false;
    btn.innerText = 'Record';

    let record = {
      project_id: projectId,
      start_time: formatDateTime(startTime),
      end_time: formatDateTime(endTime),
    };
    createRecord(record);
  }
}


// 获取所有计时按钮 
const timerBtns = document.querySelectorAll('.timer-btn');


timerBtns.forEach(btn => {
  let active = false;//每个按钮维护独立 active状态
  btn.addEventListener('click', clickHandler);
});

*/
/*
const projectCards = document.querySelectorAll('.project-card');

projectCards.forEach(card => {

  const timerBtn = card.querySelector('.timer-btn');
  //const projectId = timerBtn.getAttribute('project-id');
  let active = false;
  let startTime, endTime;
  let projectId;

  timerBtn.addEventListener('click', function() {
    projectId = card.getAttribute('data-project-id');

    if(!active){
      startTime = new Date();
      active = true;
      timerBtn.innerText = 'Stop';
    }else{
      endTime = new Date();
      active = false;
      timerBtn.innerText = 'Record';
      
      let record = {
        project_id: projectId,
        start_time: formatDateTime(startTime),
        end_time: formatDateTime(endTime),
      };
      createRecord(record);
    }
  });

});
*/
/*
let timerBtn = document.getElementById('timer-btn');
let active = false;
let startTime = null;
//let projectCard = document.getElementsByClassName('project-card');
//let projectId = projectCard.getAttribute('data-project-id')
let projectCards = document.querySelectorAll('.project-card');

projectCards.forEach(card => {
  let projectId = card.getAttribute('data-project-id');
});

timerBtn.addEventListener('click', function() {
  if (active) {
    // Start timer
    startTime = new Date();
    active = false;
    timerBtn.innerText = 'Stop';
  } else {
    // Stop timer
    let endTime = new Date();
    active = true;
    timerBtn.innerText = 'Record';
    
    let record = {
      start_time: formatDateTime(startTime),
      end_time: formatDateTime(endTime),
      project_id: projectId
    };
    createRecord(record);
    startTime = null;
  }
});


*/