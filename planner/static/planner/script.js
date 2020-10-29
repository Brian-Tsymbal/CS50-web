document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("filter__form").onsubmit = FilterAssignment;
});

function test() {
  alert('test started')
  alert('test complete')
}

//complete
function FilterAssignment() {
  const Filter = document.getElementById("filter_options").value;
  const elements = document.getElementsByClassName(Filter);
  const all = document.getElementById("AllAssignments_listed");
  const specified = document.getElementById("Specific_Assignments");
  all.style.display = 'none';
  specified.style.display = 'block';
  if (elements.length === 0) {
    document.getElementById("index_message").style.display = 'block';
    all.style.display = "block";
    return false
  } else {
    for (var x1 = 0; x1 < elements.length; x1++) {
      console.log(elements[x1].id);
      fetch(`/AllAssignment/${elements[x1].id}`)
        .then(response => response.json())
        .then(item => {
          const id = item.id
          const title = item.title;
          const type = item.type;
          const course = item.course;
          const due = item.due

          var entry = document.createElement('div');
          entry.id = `${id}-assignment`;
          entry.className = `${type}-assignment`;
          entry.style = "border-style: solid; border-width: 2px; border-color:black; padding: 5px; margin-bottom: 5px;"
          entry.innerHTML = `<div>
        <p>You have a <b>${type}: ${title}</b></p>
        <p>For: <b>${course}</b>. </p>
        <p>Finish it by: <u><b>${due}</b></u></p>
        <button id="${id}-complete" class="complete__btn" onclick="Complete('${id}')">Finished!</button>
        </div>`;
          document.querySelector("#Specific_Assignments").appendChild(entry);
        });
    }
    return false
  }
}


//complete
function SeeForm(FormTitle) {
  const Form = document.getElementById(`${FormTitle}`)
  document.getElementById("Course-form").style.display = "none";
  document.getElementById("Assignment-form").style.display = "none";
  Form.style.display = "block";
}

//complete
function ShowCourses(id) {
  const AllCourses = document.getElementsByClassName("Course_Divs");
  var x1;
  for (x1 = 0; x1 < AllCourses.length; x1++) {
    AllCourses[x1].style.display = 'none';
  }
  fetch(`/AllCourses/${id}`)
    .then(response => response.json())
    .then(item => {
      SeeCourse(item);
    });
  return false
}

//Complete
function SeeCourse(element) {
  if (element.teacher == "") {
    element.teacher = "not listed"
  }
  if (element.email == "") {
    element.email = "not listed"
  }
  if (element.room == "") {
    element.room = "not listed"
  }
  var entry = document.createElement('div');
  entry.innerHTML = `<div>
  <h1>${element.title}</h1>
  <hr>
  <p>Taught by: <b>${element.teacher}</b></p>
  <p>Email: <b>${element.email}</b></p>
  <p>This is a <b>${element.durration}</b>, <b>${element.type}</b> class.</p>
  <p>room number: <b>${element.room}</b></p >
  <button onclick="UnEnroll(${element.id})">Leave Class</button>
  </div>`;
  document.querySelector("#Course_expanded").appendChild(entry);
  document.querySelector("#Course_expanded").style.display = "block";
}


//complete
function UnEnroll(id) {
  console.log(id);
  console.log("initiated");
  fetch(`/AllCourses/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      enrolled: false
    })
  }).then(result => {
    console.log("done");
    console.log(result);
    window.location.replace('http://127.0.0.1:8000/courses');
  });
  console.log('complete');
}

//complete
function Complete(id) {
  console.log(id);
  console.log("initiated");
  fetch(`/AllAssignment/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      status: true
    })
  }).then(result => {
    console.log("done");
    console.log(result);
  })
  console.log('complete');
  var x = window.location.replace('http://127.0.0.1:8000/');
  x.reload();
}
