# Format source code automatically

style:
	black --line-length 90 --target-version py36 mctchess/*.py tests

# Run tests

test:
	python -m pytest -v ./tests/
