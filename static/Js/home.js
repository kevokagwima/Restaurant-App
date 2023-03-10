function openView(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("menu-item");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();

function menuItem(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontents");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("category");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" actives", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " actives";
}
var tablinkz;

tablinkz = document.querySelectorAll(".category");
tablinkz[0].id = "defaultOpens";

document.getElementById("defaultOpens").click();

const side_nav = document.querySelector(".side-nav");
const burger = document.querySelector(".burger");

burger.addEventListener("click", () => {
  side_nav.classList.toggle("hide-side-nav");
});
