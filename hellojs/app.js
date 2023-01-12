console.log("Hello world");

var x = 5;

var h1element = document.querySelector("#my-heading");
console.log("my h1 element", h1element);


var myButton = document.querySelector("#add-friend-button");
console.log("my button element", myButton);

myButton.onclick = function () {
  console.log("my button was clicked");
  //h1element.innerHTML = "I'm different now.";
  //h1element.style.color = "#FF0000";
  //h1element.style.backgroundColor = "#0000FF";
  
  var friendNameInput = document.querySelector("#friend-name");
  console.log("my input element:", friendNameInput);
  console.log("input element text:", friendNameInput.value);

  var myList = document.querySelector("#my-friend-list");
  console.log("my list element:", myList);

  var newItem = document.createElement("li");
  newItem.innerHTML = friendNameInput.value;
  myList.appendChild(newItem);

  friendNameInput.value = "";
};

