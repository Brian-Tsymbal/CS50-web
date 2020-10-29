
document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").onsubmit = sending_email;
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';



  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(Emails => {
        show_email(Emails, mailbox)
      });
      return false
    });
}

//sends the emails
function sending_email() {
  const receiver = document.querySelector("#compose-recipients").value;
  const title_line = document.querySelector("#compose-subject").value;
  const content = document.querySelector("#compose-body").value;


  if (receiver === "") {
    document.querySelector("#error-message").style.display = "block";
    return false;
  } else if (receiver === false) {
    alert('error');
    document.querySelector("#error-message").style.display = "block";
    return false;
  } else {
    document.querySelector("#error-message").style.display = "none";
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: receiver,
        subject: title_line,
        body: content
      })
    })
      .then(response => response.json())
      .then(result => {
        load_mailbox('sent');
        console.log(result);
      });
    return false;
  }
}

// shows the emails
function show_email(item, mailbox) {
  var entry = document.createElement('div');
  if (mailbox == "inbox") {
    entry.id = `${item.id}-inbox`;
    entry.className = `inbox`
    entry.innerHTML = `<div onclick="open_mail(${item.id})" style="border-style: solid; border-color: black; border-width: 2px; display: block;">
    Sender: ${item.sender}
    <br>
    Time: ${item.timestamp}
    <br>
    Subject: ${item.subject}
    <br>
    <hr> 
    <p> ${item.body} </p>
    </div>
    <button id="${item.id}-Reply_button" type="button" style="display: none;" onclick="replying(${item.id})">Reply</button>
    <button id="${item.id}-Archive_button" type="button" style="display: none;" onclick="archiveFunction(${item.id},true)">Archive</button>`;
    if (item.read === true) {
      entry.style.backgroundColor = "rgb(171, 173, 176)";
    }
    document.querySelector("#emails-view").appendChild(entry);
  } else if (mailbox == 'sent') {
    entry.className = `sent`
    entry.id = `${item.id}-sent`;
    entry.innerHTML = `<div style="border-style: solid; border-color: black; border-width: 2px; background-color: gray">
    Recipients: ${item.recipients}
    <br>
    Time: ${item.timestamp}
    <br>
    Subject: ${item.subject}
    </div>`;
    document.querySelector("#emails-view").appendChild(entry);
  } else {
    entry.className = `archived`
    entry.id = `${item.id}-archive`;
    entry.innerHTML = `<div style="border-style: solid; border-color: black; border-width: 2px; background-color: gray">
    Sender: ${item.sender}
    <br>
    Time: ${item.timestamp}
  <br>
  Subject: ${item.subject}
  <br>
  <hr> ${item.body}
  <br>
  <button id="Reply_button" type="button" style="display: inline-block;" onclick="replying(${item.id})">Reply</button>
  <button id="Archive_button" type="button" style="display: inline-block;" onclick="archiveFunction(${item.id},false)">Unarchive</button>
  </div>`;
    document.querySelector("#emails-view").appendChild(entry);
  }
}

//allows the user to reply to an opened email
function replying(email) {
  console.log(email);
  fetch(`/emails/${email}`)
    .then(response => response.json())
    .then(emails => {
      const Init_Sender = emails.sender;
      const timestamp = emails.timestamp;
      const subject = emails.subject;
      const body = emails.body;
      console.log('function started');
      compose_email();
      const Init_Email = `On ${timestamp} ${Init_Sender} wrote: ${body}`;
      document.querySelector("#compose-recipients").value = Init_Sender;
      document.querySelector("#compose-subject").value = subject;
      document.querySelector("#compose-body").value = Init_Email;
      console.log(emails);
    });
  return false
}

//allows the user to togle the archive status
function archiveFunction(id, state) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: state,
    }),
  }).then(result => {
    load_mailbox('inbox');
    console.log(result);
  });
  return false
}

//function that alows users to open mail
function open_mail(id) {
  const emails = document.querySelectorAll(`.inbox`);
  const active = document.getElementById(`${id}-inbox`);
  emails.forEach(Entry => {
    document.getElementById(Entry.id).style.display = "none";
  });
  console.log("all hidden");
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  active.style.display = "block";
  active.style.backgroundColor = "white";
  document.getElementById(`${id}-Reply_button`).style.display = "inline-block";
  document.getElementById(`${id}-Archive_button`).style.display = "inline-block";
}


//function for prototyping and testing aspects of code
function test(string) {
  console.log('test initiated');
  console.log(string);
  console.log('test complete');
}
