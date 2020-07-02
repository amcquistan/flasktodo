
var todoLnks = document.querySelectorAll('a[data-todo]');

for (var todoLnk of todoLnks) {
    todoLnk.addEventListener('click', evt => {
        evt.preventDefault();
        var clickedTodoId = evt.target.getAttribute('data-todo');
        console.log('Clicked for todo ' + clickedTodoId);
        for (var todoDescription of document.querySelectorAll('.todo-description')) {
            var todoId = todoDescription.getAttribute('data-description');
            console.log('Checking todo ' + todoId);
            if (!todoDescription.classList.contains('is-hidden')) {
                todoDescription.classList.add('is-hidden');
            } else if (todoId == clickedTodoId) {
                todoDescription.classList.remove('is-hidden');
            }
        }
    });
}
