# syntax=docker/dockerfile:1.9

# copy Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# - Silence uv complaining about not being able to use hard links,
# - tell uv to byte-compile packages for faster application startups,
# - prevent uv from accidentally downloading isolated Python builds,
# - and finally declare `/app` as the target for `uv sync`.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0

### End builder prep -- this is where your app Dockerfile should start.

# Set WORKINGDIR (the working directory) to /app
WORKDIR /app

# Synchronize DEPENDENCIES without the application itself.
# This layer is cached until uv.lock or pyproject.toml change, which are
# only temporarily mounted into the builder container since we don't need
# them in the production one.
# You can create `/app` using `uv venv` in a separate `RUN`
# step to have it cached, but with uv it's so fast, it's not worth
# it, so we let `uv sync` create it for us automagically.
# --mount uv.lock and pyproject.toml files
# --locked checks whether the lock file is still up to date defined by pyproject.toml
#    to use the lockfile without checking if it is up-to-date, use the --frozen option
# --no-dev used to exclude the dev group
# --no-install-project do not instll the current project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
    --locked \
    --no-dev \
    --no-install-project

# Copy files from host machine directory to /app and their corresponding
# subdirectories
COPY pyproject.toml /app/
COPY uv.lock /app/
COPY data /app/data
COPY src /app/src
COPY templates /app/templates

# Uncomment for debugging check pwd and that files are copied into /app
RUN pwd 
RUN echo "Listing files in /app:" && ls -la /app
# End debugging tools

# --locked checks whether the lock file is still up to date defined by pyproject.toml
#    to use the lockfile without checking if it is up-to-date, use the --frozen option
# --no-dev used to exclude the dev group
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --locked \
    --no-dev 

########################
## Start the FINAL stage 
## Image without uv
########################

# It is important to use the image that matches the builder because 
# the path to the Python executable must be the same
FROM python:3.13-slim-bookworm

# Don't run your app as root.
# groupadd − add (create) a new group definition on the system
#   -r , --system : create a system account 
# useradd - add user accounts to the system
#   Source: https://command-line.bazadanni.com/linux/useradd.html
#   -r , --system: create a system account 
#   -d: to add a home directory for the user
#   -g, –gid GROUP: to creates a specific id in this case `app` for the new user
#   -N, –no-user-group: do not a create a group with the same name as the user 

RUN <<EOT
groupadd -r app
useradd -r -d /app -g app -N app
EOT

# Place executables in the environment at the front of the path
# adds the application virtualenv to search path.
ENV PATH="/app/.venv/bin:$PATH"

#Add user created modules to PYTHONPATH to see if I can get modules recognized
ENV PYTHONPATH="/app:/app/data:/app/src/"

# Verify PYTHONPATH setting (optional)
RUN echo $PYTHONPATH

# Copy the pre-built `/app` directory to the runtime container
# and change the ownership to user app and group app in one step.
COPY --from=builder --chown=app:app /app /app

# Run app.py when the container launches using exec style
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80" ]