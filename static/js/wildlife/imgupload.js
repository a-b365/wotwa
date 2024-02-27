function showPreview(event){
    if(event.target.files.length > 0){
      var src = URL.createObjectURL(event.target.files[0]);
      var preview = document.getElementById("file-ip-1-preview");
      preview.src = src;
      preview.style.display = "block";
      preview.style.width = "100%";
  }
}

function hideElement(elementId){
  var element = document.getElementById(elementId);
  element.style.display = "none";

}
