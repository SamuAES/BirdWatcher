function show_comments(id) {
  var x = document.getElementById("comments"+id);
  if (x.style.display === "none") {
      x.style.display = "block";
  } else {
      x.style.display = "none";
  }
}


