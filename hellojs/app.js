console.log("Hello world");

var myFriends = ["Joe", "Steve", "John", "Sara"];

//var myObject = { "name": "apple", "color": "red" };

//var myFriends = [{
//  "name": "Joe",
//  "homeTown": "Atlanta",
//  "hobby": "tennis"
//}, {
//  "name": "Steve",
//  "homeTown": "SLC",
//  "hobby": "painting"
//}];

//var x = 5;

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

var randomButton = document.querySelector("#random-friend-button");
console.log("random button query", randomButton);

randomButton.onclick = function () {
  console.log("the random button was clicked");

  // random index for a random friend (0 to length of friends array)
  var randomIndex = Math.floor(Math.random() * myFriends.length);
  // index my array of friends: a variable with the string
  var randomName = myFriends[randomIndex];
  // query the span
  var randomNameSpan = document.querySelector("#random-friend-name");
  // assign innerHTML of the span to the friend name string
  randomNameSpan.innerHTML = randomName + " was picked.";
};
