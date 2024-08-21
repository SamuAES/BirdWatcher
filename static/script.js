function show_hide_btn(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
      x.style.display = "block";
  } else {
      x.style.display = "none";
  }
}


function edit_bio_btn(bio_id, edit_id, btn_id) {
  var bio = document.getElementById(bio_id);
  var edit = document.getElementById(edit_id);
  const button = document.getElementById(btn_id);

  if (bio.style.display === "none") {
      bio.style.display = "block";
      edit.style.display = "none";
      button.innerHTML = 'Cancel'
  } else {
      bio.style.display = "none";
      edit.style.display = "block";
      button.innerHTML = 'Edit bio'
  }
}