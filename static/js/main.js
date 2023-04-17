"use strict";

// LOGIN/SIGNUP PASSWORD
const password = document.querySelector(".pass-in");

// PASSWORD LIST PASSWORD
const passwordCellPass = document.querySelectorAll(".password-cell-pass");
const passwordBullets = document.querySelectorAll(".password-cell-hide");
const passwordShowImg = document.querySelectorAll(".password-view");
const passwordHideImg = document.querySelectorAll(".password-hide");

// ADD CTAEGORY MODAL
const addCategoryOpen = document.querySelector(".add-category");
const addCategoryClose = document.querySelector(".cancel-category");
const addCategoryModal = document.querySelector(".modal");

// ADD PASSWORD FORM
const showPass = document.querySelector(".show-pass");
const hidePass = document.querySelector(".hide-pass");
const formPass = document.querySelector(".form-pass-in");

const togglePassword = (password) => {
  if (password.type === "password") {
    password.type = "text";
  } else {
    password.type = "password";
  }
};

for (let i = 0; i < passwordShowImg.length; i++) {
  passwordShowImg[i].addEventListener("click", () => {
    passwordBullets[i].classList.remove("hidden");
    passwordCellPass[i].classList.add("hidden");
    passwordShowImg[i].classList.add("hidden");
    passwordHideImg[i].classList.remove("hidden");
  });
}

for (let i = 0; i < passwordHideImg.length; i++) {
  passwordHideImg[i].addEventListener("click", () => {
    passwordBullets[i].classList.add("hidden");
    passwordCellPass[i].classList.remove("hidden");
    passwordShowImg[i].classList.remove("hidden");
    passwordHideImg[i].classList.add("hidden");
  });
}

addCategoryOpen &&
  addCategoryOpen.addEventListener("click", () => {
    addCategoryModal.showModal();
  });

addCategoryClose &&
  addCategoryClose.addEventListener("click", () => {
    addCategoryModal.close();
  });

showPass &&
  showPass.addEventListener("click", () => {
    togglePassword(formPass);
    showPass.classList.add("hidden");
    hidePass.classList.remove("hidden");
  });
hidePass &&
  hidePass.addEventListener("click", () => {
    togglePassword(formPass);
    hidePass.classList.add("hidden");
    showPass.classList.remove("hidden");
  });

// HIGHLIGHT CATEGORIES ON CLICK BY GATHERING DATA FROM URL
const paramString = window.location.href.split("?")[1];
const queryString = new URLSearchParams(paramString);
const categoryItem = document.querySelectorAll(".category-name");

let text = "";
let categoryToBeActive = "";

for (let pair of queryString.entries()) {
  text = pair[1];
}

for (let i = 0; i < categoryItem.length; i++) {
  if (categoryItem[i].innerHTML === text) {
    categoryToBeActive = categoryItem[i];
    break;
  }
}

if (categoryToBeActive === "") {
  if (categoryItem[0]) categoryItem[0].className += " cat-active";
} else {
  categoryToBeActive.className += " cat-active";
}

// HIGHLIGHT OPTION ON CLICK BY GATHERING DATA FROM URL
const urlStr = window.location.href;

if (urlStr.includes("edit-profile")) {
  document.querySelector(".pass-op").className = document
    .querySelector(".pass-op")
    .className.replace(" op-active", "");
  document.querySelector(".edit-profile-op").className += " op-active";
}

// COPY PASSWORD TO CLIPBOARD
const savedPassword = document.querySelectorAll(".password-cell-pass");
const passwordCopy = document.querySelectorAll(".password-copy");

for (let i = 0; i < savedPassword.length; i++) {
  passwordCopy[i].addEventListener("click", () => {
    const toast = document.getElementById("snackbar");
    toast.className = "show";

    setTimeout(function () {
      toast.className = toast.className.replace("show", "");
    }, 3000);

    navigator.clipboard.writeText(savedPassword[i].textContent);
  });
}
