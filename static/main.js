
//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag   = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
    e.preventDefault();
    e.stopPropagation();

    fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}


function fileSelectHandler(e) {
    var files = e.target.files || e.dataTransfer.files;
    fileDragHover(e);
    for (var i = 0, f; (f = files[i]); i++) {
      previewFile(f);
    }
  }

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview")
var imageDisplay = document.getElementById("image-display")
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var textResult = document.getElementById("show-result-text");
var loader = document.getElementById("loader");

function submitImage() {
  console.log("submit");

  if (!imageDisplay.src || !imageDisplay.src.startsWith("data")) {
    window.alert("Please select an image before submit.");
    return;
  }

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  predictImage(imageDisplay.src);
}

function clearImage() {
  fileSelect.value = "";

  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";
  textResult.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}

function previewFile(file) {
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    textResult.innerHTML = "";
    imageDisplay.classList.remove("loading");

    displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(image)
  })
  .then(resp => {
    if (resp.ok)
      resp.json().then(data => { hide(loader); displayResult(data); });
  })
  .catch(err => {
    console.log("An error occured", err.message);
    window.alert("Oops! Something went wrong.");
  });
}

function displayImage(image, id) {
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // console.log(data.result)
  data.result.forEach(function(item) { 
    const postText = document.createElement("p");
    postText.textContent = ` result id: ${item.id}, messege:  ${item.text} , score: ${item.score} % ` 
    textResult.appendChild(postText)
    show(textResult);
  })
}

function drowBox(box) { 
  var ctx = canvas.getContext("2d");
  var ctxo = overlay.getContext("2d");

  ctx.strokeStyle = "blue";
  ctx.lineWidth = 3;
  ctxo.strokeStyle = "blue";
  ctxo.lineWidth = 3;
}

function hide(el) {
  el.classList.add("hidden");
}

function show(el) {
  el.classList.remove("hidden");
}