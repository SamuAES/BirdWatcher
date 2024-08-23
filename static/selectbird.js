const wrapper2 = document.querySelector(".wrapper2"),
selectBtn = wrapper2.querySelector(".select-btn"),
searchInp = wrapper2.querySelector("input"),
options = wrapper2.querySelector(".options");


function addBird(selectedBird) {
    options.innerHTML = "";
    birdlist.forEach(bird => {
        let isSelected = bird == selectedBird ? "selected" : "";
        let li = `<li onclick="updateName(this)" class="${isSelected}">${bird}</li>`;
        options.insertAdjacentHTML("beforeend", li);
    });
}
addBird();
function updateName(selectedLi) {
    searchInp.value = "";
    addBird(selectedLi.innerText);
    wrapper2.classList.remove("active");
    selectBtn.firstElementChild.innerText = selectedLi.innerText;
    document.getElementById("hiddenInput").value = selectedLi.innerText;
}
searchInp.addEventListener("keyup", () => {
    let arr = [];
    let searchWord = searchInp.value.toLowerCase();
    arr = birdlist.filter(data => {
        return data.toLowerCase().startsWith(searchWord);
    }).map(data => {
        let isSelected = data == selectBtn.firstElementChild.innerText ? "selected" : "";
        return `<li onclick="updateName(this)" class="${isSelected}">${data}</li>`;
    }).join("");
    options.innerHTML = arr ? arr : `<p style="margin-top: 10px;">Oops! Bird not found</p>`;
});
selectBtn.addEventListener("click", () => wrapper2.classList.toggle("active"));


