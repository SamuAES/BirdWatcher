
function show_hide_btn(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
      x.style.display = "block";
  } else {
      x.style.display = "none";
  }
}

function topnav_activate(id) {
  var current_page = document.getElementById(id)
  current_page.classList.toggle("active")
}


function edit_profile_btn(profile_card, edit_profile_card) {
  var profile_card = document.getElementById(profile_card);
  var edit_profile_card = document.getElementById(edit_profile_card);

  if (profile_card.style.display === "block") {
      profile_card.style.display = "none";
      edit_profile_card.style.display = "block";
  } else {
      profile_card.style.display = "block";
      edit_profile_card.style.display = "none";
  }
}