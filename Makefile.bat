@ECHO OFF
set argtype=%1

set PYTHON_VENV="%cd%\.venv\"
set PYTHON="%cd%\.venv\Scripts\python.exe"


IF "%argtype%"=="qas" (
	CALL :BlackLinter
	echo:
	CALL :IsortLinter
	echo:
	CALL :AutoflakeLinter
	echo:
	CALL :PyprojectCheck
	echo:
	CALL :UnitTests
    EXIT /B 0
)

IF "%argtype%"=="black" (
	CALL :BlackLinter
    EXIT /B 0
)

IF "%argtype%"=="isort" (
	CALL :IsortLinter
    EXIT /B 0
)

IF "%argtype%"=="autoflake" (
	CALL :AutoflakeLinter
    EXIT /B 0
)

IF "%argtype%"=="tests" (
	CALL :UnitTests
    EXIT /B 0
)

IF "%argtype%"=="poetry_check" (
	CALL :PyprojectCheck
    EXIT /B 0
)

echo make: *** No rule to make target '%argtype%'. Stop.
EXIT /B 1


:BlackLinter
echo # Running black Linter #
%PYTHON% -m black --config="pyproject.toml" .
EXIT /B 0

:IsortLinter
echo # Running isort linter #
%PYTHON% -m isort --settings-path="pyproject.toml" .
EXIT /B 0

:AutoflakeLinter
echo # Running QAS autoflake #
%PYTHON% -m autoflake -i -r --exclude=.venv/*,venv/*,.pytest_cache/* --remove-unused-variables --remove-all-unused-imports --remove-duplicate-keys --expand-star-imports .
EXIT /B 0

:UnitTests
echo # Running Unit Tests #
%PYTHON% -m pytest -ra -x -q -v -s --cov=py2Solve --ignore-glob=.venv/*,venv/*,.pytest_cache/* --cov-report term-missing --color=yes --cov-fail-under=20
EXIT /B 0

:PyprojectCheck
echo # Running pyproject.toml check #
%PYTHON% -m poetry check
EXIT /B 0

