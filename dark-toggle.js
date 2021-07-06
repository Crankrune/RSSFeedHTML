function darkToggle() {
    var element = document.body;
    if (element.classList.contains("dark-grey")) {
        element.classList.remove("dark-grey");
        element.classList.add("dark-twitter");
    } else if (element.classList.contains("dark-twitter")) {
        element.classList.remove("dark-twitter");
        element.classList.add("light-mode");
    } else if (element.classList.contains("light-mode")) {
        element.classList.remove("light-mode");
        element.classList.add("dark-grey");
    }
}