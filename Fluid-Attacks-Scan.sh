#!/bin/bash
docker run -v ~/github/H2DatabaseOOo:/working-dir ghcr.io/fluidattacks/makes/amd64 m gitlab:fluidattacks/universe@trunk /skims scan ./_fascan.yml
docker system prune -f
