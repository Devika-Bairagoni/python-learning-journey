# Reviewing what I know about variables

server_name = "api-server-01"
server_port = 8000
is_running = True
cpu_usage = 92.3

print(server_name)
print(server_port)
print(is_running)
print(cpu_usage)
# Printing with f-strings
print(f"Server: {server_name}")
print(f"Port: {server_port}")
print(f"Running: {is_running}")
print(f"CPU Usage: {cpu_usage}%")
# Checking server health
if cpu_usage > 80:
    print("WARNING: CPU is too high")
else:
    print("CPU is normal")