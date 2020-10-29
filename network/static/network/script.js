

//works
function SeeProfile(id) {
  window.location.href = `http://127.0.0.1:8000/UserProfile/${id}`;
}

//works
function follow(id) {
  fetch(`AllFollowers/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      true: false
    }),
  }).then(result => {
    console.log("unfollowed");
    console.log(result)
    window.location.href = `http://127.0.0.1:8000/UserProfile/${id}`;
  });
  return false
}

//works
function Likepost(id) {
  console.log(id);
  const item = document.getElementById(`${id}_like_value`);
  var like = item.innerText;
  like++;
  item.innerText = like;
  fetch(`/AllPosts/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      likes: item.innerText,
    }),
  }).then(result => {
    console.log("finished");
    console.log(result);
  });
  return false
}

//works
function DislikePost(id) {
  console.log(id);
  const item = document.getElementById(`${id}_like_value`);
  var like = item.innerText;
  like--;
  if (like > -1) {
    item.innerText = like;
    fetch(`/AllPosts/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        likes: item.innerText,
      }),
    }).then(result => {
      console.log("finished");
      console.log(result);
    });
    return false
  } else {
    console.log("can't have less than 0 likes");
  }

}

//works
function editpost(id) {
  const update = document.getElementById(`edit_answer:${id}`);
  const initial = document.getElementById(`${id}_content`).innerText;
  document.getElementById(`edit_form:${id}`).style.display = 'block';
  document.getElementById(`edit_form:${id}`).style.width = 'widget';
  update.value = initial;
  console.log(id);
  document.getElementById(`edit_answer:${id}_submit`).addEventListener('click', function () {
    UpdateBody(id);
  });
}

//works
function UpdateBody(id) {
  const initial = document.getElementById(`edit_answer:${id}`).value;
  console.log(initial);
  console.log(id);
  fetch(`AllPosts/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      body: initial
    })
  }).then(result => {
    console.log("updated");
    console.log(result);
  });
  return false
}


