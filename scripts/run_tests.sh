#!/bin/bash
set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

flake8 .
display_result $? 1 "Code style check"

## Code coverage
py.test --cov=app --cov-report=term-missing tests/ --strict -v
