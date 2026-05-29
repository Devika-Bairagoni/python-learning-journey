# Reviewing what I know about variables

server_name = "api-server-01"
server_port = 8000
is_running = True
cpu_usage = 45.6

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
    # A simple function I wrote myself
def check_server_health(name, cpu):
    if cpu > 80:
        print(f"ALERT: {name} CPU is {cpu}% - needs attention")
    elif cpu > 60:
        print(f"WARNING: {name} CPU is {cpu}% - watch closely")
    else:
        print(f"OK: {name} CPU is {cpu}% - healthy")

check_server_health("api-server-01", 45.6)
check_server_health("db-server-01", 92.3)
check_server_health("cache-01", 78.1)

def  check_memory_health(name,memory_used_percent):
    if memory_used_percent > 90:
        print(f"ALERT: {name} Memory usage is {memory_used_percent}% - needs attention")
    elif memory_used_percent > 70:
        print(f"WARNING: {name} Memory usage is {memory_used_percent}% - watch closely")
    else:
        print(f"OK: {name} Memory usage is {memory_used_percent}% - healthy")
check_memory_health("api-server-01", 55.0)
check_memory_health("db-server-01", 87.3)
check_memory_health("cache-01", 94.1)