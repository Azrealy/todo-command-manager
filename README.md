# Todo manager CLI

Handle the basic CRUD database execution of todo cmd.

# Setup todo cmd

```bash
sudo python3.6 setup.py install
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
When use the `add` subcommand text type arguments should be setted. 
```bash
$todo add "Say Hello."
Task has been added scucessfully.
1 | Say Hello.
```

## Delete todo task
When use the `delete` subcommand int type argument should be setted. 
```bash
$todo delete 1
Task 1 is deleted sucessfully.
```
## Update todo task
When use the `update` subcommand arguments of option `-i` and `-t` should be setted. 
```bash
$todo update -i 1 -t "Say Bye"
The Context of task 1 has changed to "Say Bye".
```
## Show todo task
`Show` subcommand has three option `-c`, `-i`, `-a` use to show defferent task status list.
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
When use the `delete` subcommand int type argument should be setted. 
```bash
$todo complete 1
Task 1 complete.
```

# Pytest

This package implement UT, IT test. You can use the following cmd to execute pytest.

```bash
pytest todo/tests
```

