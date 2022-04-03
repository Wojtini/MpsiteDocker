var coll = document.getElementsByClassName("collapsible");
var i;

function openCity(evt, name) {
    console.log(name);
  var i, tabcontent, tablinks, buttons;
  tabcontent = document.getElementsByClassName("tank_container");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  buttons = document.getElementsByClassName("tablinks");
  for (i = 0; i < buttons.length; i++) {
    if (buttons[i].id == 'button_' + name){
        buttons[i].style.backgroundColor = "#212121";
    }else{
        buttons[i].style.backgroundColor = "gray";
    }
  }

  tablinks = document.getElementsByClassName("tank_container");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(name).style.display = "grid";
  evt.currentTarget.className += " active";
}