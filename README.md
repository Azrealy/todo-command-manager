# Todo manager CLI

Handle the basic CRUD database execution of todo cmd.

# Setup todo cmd

```bash
sudo python3.6 setup.py install
```

# Usage of Todo cmd

```bash
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

# Pytest

This package implement UT, IT test. You can use the following cmd to execute pytest.

```bash
pytest todo/tests
```

