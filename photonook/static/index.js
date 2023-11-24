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

function comment(postId, input) {
  const commentBlock = document.getElementById(`comment-block-${postId}`);
  const text = input.value;

  fetch(`/comment/${postId}`, { method: "POST", body: JSON.stringify({ text }) })
    .then((res) => res.json())
    .then((data) => {
      input.value = "";

      const newComment = commentBlock.cloneNode(true);
      newComment.className = "mb-1 d-block"
      newComment.removeAttribute('id');

      //<a>
      newComment.children[0].href = "/profile/" + data["user_id"];
      newComment.children[0].children[0].innerHTML = "@" + data["user_username"];

      // <span>
      newComment.children[1].innerHTML = data["comment_text"];

      const parentElement = commentBlock.parentElement;
      parentElement.insertBefore(newComment, parentElement.lastElementChild);
    })
    .catch((e) => {
      console.log(e)
      alert("Could not comment post.")
    });
}