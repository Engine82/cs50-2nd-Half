document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.topButton').onclick = function() {
        document.documentElement.scrollTop = 0;
    }
});