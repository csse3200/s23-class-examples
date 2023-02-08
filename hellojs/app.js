console.log("Hello world");

//var myMovies = ["Joe", "Steve", "John", "Sara"];
var myMovies = [];

//var myObject = { "name": "apple", "color": "red" };

//var myMovies = [{
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


var addButton = document.querySelector("#add-movie-button");
console.log("my button element", addButton);

addButton.onclick = function () {
  console.log("my button was clicked");
  //h1element.innerHTML = "I'm different now.";
  //h1element.style.color = "#FF0000";
  //h1element.style.backgroundColor = "#0000FF";
  
  var movieNameInput = document.querySelector("#movie-name");
  console.log("my input element:", movieNameInput);
  console.log("input element text:", movieNameInput.value);

  createMovieOnServer(movieNameInput.value);

  movieNameInput.value = "";
};

var randomButton = document.querySelector("#random-movie-button");
console.log("random button query", randomButton);

randomButton.onclick = function () {
  console.log("the random button was clicked");

  // random index for a random movie (0 to length of movies array)
  var randomIndex = Math.floor(Math.random() * myMovies.length);
  // index my array of movies: a variable with the string
  var randomName = myMovies[randomIndex];
  // query the span
  var randomNameSpan = document.querySelector("#random-movie-name");
  // assign innerHTML of the span to the movie name string
  randomNameSpan.innerHTML = randomName + " was picked.";
};

function loadMoviesFromServer() {
  fetch("http://localhost:8080/movies").then(function (response) {
    response.json().then(function (data) {
      console.log("data received from server:", data);
      myMovies = data;

      var myList = document.querySelector("#my-movie-list");
      console.log("my list element:", myList);
      myList.innerHTML = "";

      // for movie in myMovies:
      myMovies.forEach(function (movie) {
        var newItem = document.createElement("li");

        var nameDiv = document.createElement("div");
        nameDiv.innerHTML = movie;
        nameDiv.classList.add("movie-name");
        newItem.appendChild(nameDiv);

        var dateDiv = document.createElement("div");
        dateDiv.innerHTML = "1990";
        dateDiv.classList.add("movie-date");
        newItem.appendChild(dateDiv);

        myList.appendChild(newItem);
      });
    });
  });
}

function createMovieOnServer(movieName) {
  console.log("attempting to create movie", movieName, "on server");

  var data = "name=" + encodeURIComponent(movieName);
  console.log("sending data to server:", data);

  fetch("http://localhost:8080/movies", {
    // request details:
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  }).then(function (response) {
    // when the server responds:

    if (response.status == 201) {
      loadMoviesFromServer();
    } else {
      console.log("server responded with", response.status, "when trying to create a movie");
    }

  });
}

loadMoviesFromServer();
