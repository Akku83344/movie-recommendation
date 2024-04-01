document.addEventListener("DOMContentLoaded", function () {
  const movieSelect = document.getElementById("movieSelect");
  const recommendButton = document.getElementById("recommendButton");
  const recommendationsContainer = document.getElementById("recommendations");

  // Populate movie dropdown
  fetch("https://movie-recommeder-system-j4gd.onrender.com/api/movie_list")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      data.movie_list.forEach((movie) => {
        const option = document.createElement("option");
        option.value = movie;
        option.textContent = movie;
        movieSelect.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching movie list:", error));

  // Event listener for recommend button
  recommendButton.addEventListener("click", function () {
    const selectedMovie = movieSelect.value;
    if (selectedMovie) {
      fetch("https://movie-recommeder-system-j4gd.onrender.com/api/recommendations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ selected_movie: selectedMovie }),
      })
        .then((response) => response.json())
        .then((data) => {
          recommendationsContainer.innerHTML = ""; // Clear previous recommendations
          data.recommended_movie_names.forEach((name, index) => {
            const recommendation = document.createElement("div");
            recommendation.className = "recommendation";
            recommendation.innerHTML = `<p>${name}</p><img src="${data.recommended_movie_posters[index]}" alt="${name}">`;
            recommendationsContainer.appendChild(recommendation);
          });
        })
        .catch((error) =>
          console.error("Error fetching recommendations:", error)
        );
    } else {
      alert("Please select a movie");
    }
  });
});
