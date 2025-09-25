#!/bin/bash

# Start Supervisor in the background
supervisord -c /etc/supervisor/supervisord.conf

# Wait for Supervisor to fully initialize and start processes
# (You might need to adjust this delay or add a more robust health check)
sleep 5

# Keep the container running and provide an interactive shell
# This allows you to run commands directly in the terminal
exec "$@" 