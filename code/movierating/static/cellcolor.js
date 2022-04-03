const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));


function calculateGradient(rating){
    color0 = '#000000'
    color20 = '#ff0000'
    color50 = '#efff00'
    color65 = '#00ff0e'
    color90 = '#00dadb'
    color100 = '#ff00ef'

    if (rating >= 90 && rating <= 100){
        ratio = (rating-90)/(100-90)
        return getRGB(color90,color100,ratio)
    } else if (rating >= 65 && rating < 90){
        ratio = (rating-65)/(90-65)
        return getRGB(color65,color90,ratio)
    } else if (rating >= 50 && rating < 65){
        ratio = (rating-50)/(65-50)
        return getRGB(color50,color65,ratio)
    } else if (rating >= 20 && rating < 50){
        ratio = (rating-20)/(50-20)
        return getRGB(color20,color50,ratio)
    } else if (rating >= 0 && rating < 20){
        ratio = (rating-0)/(20-0)
        return getRGB(color0,color20,ratio)
    }
}

function getRGB(color1,color2,ratio){
    var r1 = parseInt(color1.substring(1,3),16)
    var g1 = parseInt(color1.substring(3,5),16)
    var b1 = parseInt(color1.substring(5,7),16)

    var r2 = parseInt(color2.substring(1,3),16)
    var g2 = parseInt(color2.substring(3,5),16)
    var b2 = parseInt(color2.substring(5,7),16)

    var newR = Math.ceil(r1 * (1-ratio) + r2 * ratio)
    var newG = Math.ceil(g1 * (1-ratio) + g2 * ratio)
    var newB = Math.ceil(b1 * (1-ratio) + b2 * ratio)
    var retVal = "rgb(" + newR.toString() + "," + newG.toString() + "," + newB.toString() + ")"
    return retVal
}

$(document).ready(function(){
    $('#spreadsheet td.rating_cell').each(function(){
        if ($(this).text() != ''){
            rating = parseInt($(this).text())
            color = calculateGradient(rating)
            $(this).css('background-color',color);
        } else {
            $(this).css('background-color','black');
        }
    });
    $('#ratingscale td.gradient').each(function(){
        console.log(this.id);
        rating = parseFloat(this.id)
        color = calculateGradient(rating)
        $(this).css('background-color',color);
    });

<!--    document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {-->
<!--    console.log(th);-->
<!--    const table = th.closest('table');-->
<!--    Array.from(table.querySelectorAll('tr:nth-child(n+2)'))-->
<!--        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))-->
<!--        .forEach(tr => table.appendChild(tr) );-->
<!--})));-->
});

function myFunction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("spreadsheet");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}