function like(postId) {
  const likeButton = document.getElementById(`like-button-${postId}`);

  fetch(`/like/${postId}`, { method: "PATCH" })
    .then((res) => res.json())
    .then((data) => {
      likeButton.children[1].innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "btn btn-lg p-0 text-danger";
        likeButton.children[0].className = "bi bi-heart-fill";
      } else {
        likeButton.className = "btn btn-lg p-0";
        likeButton.children[0].className = "bi bi-heart";
      }
    })
    .catch((e) => {
      console.log(e)
      alert("Could not like post.")
    });
}