# Todo manager CLI

Handle the basic CRUD database manipulation for `todo` cmd.

# Setup todo cmd

```bash
python3.6 setup.py install
```

# Usage of Todo cmd

```bash
$ todo --help
usage: todo [-h] [--init] {add,delete,update,show,complete} ...

Todo list manager

positional arguments:
  {add,delete,update,show,complete}
                        sub-command of Todo List manager help
    add                 Add a task to the todo list
    delete              Delete a task in the todo list.
    update              Update a task to the todo list.
    show                Show the todo list.
    complete            Mark a task as complete.

optional arguments:
  -h, --help            show this help message and exit
  --init                Initialize table of the database.
```

## Add todo task
When use the `add` sub-command text type arguments should be given. When implement todo creation, the `Created` time will be record.
```bash
$todo add "Say Hello."
Task has been added successfully.
1 | Say Hello. (Created At: 1 mins ago, Updated At: )
```

## Delete todo task
When use the `delete` sub-command int type argument should be given. When implement todo deletion, the `Update` time will be record.
```bash
$todo delete 1
Task 1 is deleted successfully.
```
## Update todo task
When use the `update` sub-command arguments of option `-i` and `-t` should be given. When implement todo update, the `Update` time will be record.
```bash
$todo update -i 1 -t "Say Bye"
The Context of task 1 has changed to "Say Bye".
```
## Show todo task
`Show` sub-command has three option `-c`, `-i`, `-a` use to show different task status list.
```bash
$todo show --all
1 | A task has completed
2 | A task still in progress

$todo show --incomplete
2 | A task still in progress

$todo show --complete
1 | A task has completed
```
## Complete todo task
When use the `delete` sub-command int type argument should be given. 
```bash
$todo complete 1
Task 1 complete.
```

# Pytest

This package implement UT, IT test. You can use the following cmd to execute pytest.

```bash
pytest todo/tests
```

