from setuptools import setup

setup(
	name='todocli',
	version='0.0.1',
	py_modules=['todo.todo', 'todo.model', 'todo.app', 'todo.cmd_parser'],
	entry_points={
		'console_scripts': [
			'todo = todo.app:main'
		]
	},
	test_suite='tests',
	python_requires='>=3',
	author='k-fang',
	author_email='k-fang@com',
	description='A command line todo list manager',
	keywords='command line todo list',
	url='https://todo'
)