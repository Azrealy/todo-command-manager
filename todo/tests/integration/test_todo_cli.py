# -*- coding: utf-8 -*-
import pytest
import subprocess
from todo.todo import Todo


@pytest.fixture(scope='function', autouse=True)
def setup_table():
    """
    Sets up todo list table.
    """
    yield
    args = ['todo', '-f', 'file:/tmp/data-test.db', '--init']
    p = subprocess.Popen(args)
    p.communicate()


def test_todo_cli_when_no_arguments_set():
    """
    Test 'todo' command without give arguments.
    """
    # run command
    args = ['todo']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stderr
    cmd_output = str(stdout, encoding='utf-8')
    message = 'usage: todo [-h] [--init] [-f FILE_PATH]'
    assert message in cmd_output


def test_todo_cli_add_subcommand_with_set_text():
    """
    Test 'todo add' command with context.
    """
    # run command
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'add', 'hello world']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = 'Task has been added successfully.\n' + \
        '1 | hello world (Created At: 1 mins ago, Updated At: )\n'
    assert message == cmd_output


def test_todo_cli_add_subcommand_without_set_text():
    """
    Test 'todo add' command without context.
    """
    # run command without set text
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'add']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stderr
    cmd_output = str(stderr, encoding='utf-8')
    message = 'the following arguments are required: add-text'
    assert message in cmd_output


def test_todo_cli_delete_command_when_id_not_int():
    """
    Test 'todo add' command when set id not int type.
    """
    # delete task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'delete', 'one']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stdout
    cmd_output = str(stderr, encoding='utf-8')
    message = "invalid int value: 'one'"
    assert message in cmd_output


def test_todo_cli_delete_command_when_task_exist():
    """
    Test 'todo add' command when task exist.
    """
    # add task to todo list
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'add', 'hello world']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # delete task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'delete', '1']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = 'Task 1 is deleted successfully.\n'
    assert message == cmd_output


def test_todo_cli_delete_command_when_task_not_exist():
    """
    Test 'todo add' command when task not exist.
    """
    # delete not exist task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'delete', '1']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check std
    cmd_output = str(stderr, encoding='utf-8')
    message = 'This id of task not exist.\n'
    assert message == cmd_output


def test_todo_cli_update_command_when_task_exist():
    """
    Test 'todo add' command when task exist.
    """
    # add task to todo list
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'add', 'hello world']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # update task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'update', '-i', '1', '-t', 'hello japan']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = 'The text of task 1 has changed to "hello japan".\n'
    assert message == cmd_output


def test_todo_cli_update_command_when_task_not_exist():
    """
    Test 'todo add' command when task not exist.
    """
    # update task which not exit.
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'update', '-i', '1', '-t', 'hello japan']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stdout
    cmd_output = str(stderr, encoding='utf-8')
    message = 'This id of task not exist.\n'
    assert message == cmd_output


def test_todo_cli_update_command_when_get_error():
    """
    Test 'todo add' command when arise error of command option.
    """
    # update task no option `-i`
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'update', '-t', 'hello japan']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stdout
    cmd_output = str(stderr, encoding='utf-8')
    message = 'the following arguments are required: -i/--update-task-id'
    assert message in cmd_output

    # update task no option `-t`
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'update', '-i', '1']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stdout
    cmd_output = str(stderr, encoding='utf-8')
    message = 'the following arguments are required: -t/--update-task-text'
    assert message in cmd_output

    # update task option `-i` is not int type
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'update', '-i', 'one']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stdout
    cmd_output = str(stderr, encoding='utf-8')
    message = "invalid int value: 'one'"
    assert message in cmd_output


def test_todo_cli_complete_command_when_task_not_exist():
    """
    Test 'todo complete' command when task not exist.
    """
    # complete not exist task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'complete', '1']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 2

    # check stdout
    cmd_output = str(stderr, encoding='utf-8')
    message = 'This id of task not exist.\n'
    assert message == cmd_output


def test_todo_cli_complete_command_when_task_exist():
    """
    Test 'todo complete' command when task exist.
    """
    # add task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'add', 'hello world']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # complete exist task
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'complete', '1']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = 'Task 1 complete.\n'
    assert message == cmd_output

    # check task status changed
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'show', '-c']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = '1 | hello world (Created At: 1 mins ago, Updated At: 1 mins ago)\n'
    assert message == cmd_output


def test_todo_cli_show_command_when_task_exist():
    """
    Test 'todo complete' command when task exist.
    """
    # add two task to todo list
    args = [['todo', '-f', 'file:/tmp/data-test.db', 'add', 'task will complete'],
            ['todo', '-f', 'file:/tmp/data-test.db', 'add', 'task still incomplete']]
    for i in args:
        p = subprocess.Popen(i, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

    # complete task 1
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'complete', '1']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # show all the tasks in todo list
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'show', '-a']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = '1 | task will complete (Created At: 1 mins ago, Updated At: 1 mins ago)\n' + \
        '2 | task still incomplete (Created At: 1 mins ago, Updated At: )\n'
    assert message == cmd_output

    # show the tasks status is incomplete
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'show', '-i']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = '2 | task still incomplete (Created At: 1 mins ago, Updated At: )\n'
    assert message == cmd_output

    # show the tasks status is complete
    args = ['todo', '-f', 'file:/tmp/data-test.db', 'show', '-c']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # check return code
    assert p.returncode == 0

    # check stdout
    cmd_output = str(stdout, encoding='utf-8')
    message = '1 | task will complete (Created At: 1 mins ago, Updated At: 1 mins ago)\n'
    assert message == cmd_output
    
