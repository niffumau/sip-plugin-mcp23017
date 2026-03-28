#!/bin/bash

# vim: ts=3 sw=3 sts=3 sr noet

git checkout dev
git fetch origin
git merge origin/master
git push origin dev


