from pathlib import Path

files = {}

# ── File 1: oop_basics.py ──────────────────────────────────────────

files["fundamentals/oop/oop_basics.py"] = """
class Server:
    # Class variable: shared across ALL instances
    # Use for constants or shared state
    MAX_CPU_THRESHOLD = 90.0

    def __init__(self, server_id, name, region, ip_address):
        # Instance variables: unique to EACH instance
        # __init__ runs automatically when you create an object
        self.server_id  = server_id
        self.name       = name
        self.region     = region
        self.ip_address = ip_address
        self.status     = "stopped"   # default state
        self.cpu_usage  = 0.0
        self.uptime_days = 0

    # Instance method: operates on this specific object
    def start(self):
        if self.status == "running":
            print(f"  {self.name} is already running.")
            return
        self.status = "running"
        print(f"  {self.name} started successfully.")

    def stop(self):
        if self.status == "stopped":
            print(f"  {self.name} is already stopped.")
            return
        self.status    = "stopped"
        self.cpu_usage = 0.0
        print(f"  {self.name} stopped.")

    def update_cpu(self, usage):
        if not (0.0 <= usage <= 100.0):
            raise ValueError(f"CPU usage must be 0-100, got {usage}")
        self.cpu_usage = usage
        if self.cpu_usage > self.MAX_CPU_THRESHOLD:
            print(f"  WARNING: {self.name} CPU critical: {self.cpu_usage}%")

    def is_healthy(self):
        return self.status == "running" and self.cpu_usage < self.MAX_CPU_THRESHOLD

    # __str__: what prints when you do print(server)
    def __str__(self):
        return (
            f"Server({self.server_id}) | {self.name} | "
            f"{self.region} | {self.status} | CPU: {self.cpu_usage}%"
        )

    # __repr__: what shows in debugger and logs
    def __repr__(self):
        return f"Server(id={self.server_id!r}, name={self.name!r})"


# --- Using the class ---
print("=== Creating Server Objects ===")
api_server = Server("srv-001", "api-server-01", "us-east-1", "192.168.1.10")
db_server  = Server("srv-002", "db-server-01",  "us-east-1", "192.168.1.11")

print(api_server)
print(db_server)

print("\\n=== Starting Servers ===")
api_server.start()
db_server.start()
api_server.start()   # already running

print("\\n=== Updating CPU ===")
api_server.update_cpu(45.2)
db_server.update_cpu(92.5)   # triggers warning

print("\\n=== Health Checks ===")
for server in [api_server, db_server]:
    status = "healthy" if server.is_healthy() else "unhealthy"
    print(f"  {server.name}: {status}")

print("\\n=== Stopping a Server ===")
api_server.stop()
print(api_server)
""".strip()

# ── File 2: oop_inheritance.py ─────────────────────────────────────

files["fundamentals/oop/oop_inheritance.py"] = """
class Server:
    MAX_CPU_THRESHOLD = 90.0

    def __init__(self, server_id, name, region):
        self.server_id = server_id
        self.name      = name
        self.region    = region
        self.status    = "stopped"
        self.cpu_usage = 0.0

    def start(self):
        self.status = "running"
        print(f"  {self.name} started.")

    def stop(self):
        self.status    = "stopped"
        self.cpu_usage = 0.0
        print(f"  {self.name} stopped.")

    def is_healthy(self):
        return self.status == "running" and self.cpu_usage < self.MAX_CPU_THRESHOLD

    def __str__(self):
        return f"{self.name} | {self.status} | CPU: {self.cpu_usage}%"


# --- Inheritance: child class inherits from parent ---
# DatabaseServer IS a Server, but with extra database-specific behavior.
# Use inheritance when: child IS-A parent type.

class DatabaseServer(Server):
    def __init__(self, server_id, name, region, db_engine, db_name):
        # Call parent __init__ first
        super().__init__(server_id, name, region)
        # Then add child-specific attributes
        self.db_engine     = db_engine
        self.db_name       = db_name
        self.connections   = 0
        self.max_connections = 100

    def connect(self):
        if self.connections >= self.max_connections:
            raise ConnectionError(
                f"{self.name}: max connections ({self.max_connections}) reached"
            )
        self.connections += 1
        print(f"  {self.name}: connection {self.connections} opened.")

    def disconnect(self):
        if self.connections > 0:
            self.connections -= 1
        print(f"  {self.name}: connection closed. Active: {self.connections}")

    # Override parent method to add extra behavior
    def is_healthy(self):
        parent_healthy = super().is_healthy()
        return parent_healthy and self.connections < self.max_connections

    def __str__(self):
        return (
            f"{self.name} ({self.db_engine}/{self.db_name}) | "
            f"{self.status} | connections: {self.connections}"
        )


class CacheServer(Server):
    def __init__(self, server_id, name, region, memory_gb):
        super().__init__(server_id, name, region)
        self.memory_gb    = memory_gb
        self.cache_hits   = 0
        self.cache_misses = 0

    def hit(self):
        self.cache_hits += 1

    def miss(self):
        self.cache_misses += 1

    def hit_rate(self):
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return round((self.cache_hits / total) * 100, 2)

    def __str__(self):
        return (
            f"{self.name} | {self.status} | "
            f"hit rate: {self.hit_rate()}% | memory: {self.memory_gb}GB"
        )


# --- Polymorphism: same method, different behavior ---
# All these objects are Servers, but each responds differently to is_healthy()

print("=== Inheritance Demo ===")
db = DatabaseServer("srv-002", "db-server-01", "us-east-1", "PostgreSQL", "prod_db")
cache = CacheServer("srv-003", "cache-01", "us-west-2", 8)

db.start()
cache.start()

db.connect()
db.connect()
db.connect()

cache.hit()
cache.hit()
cache.miss()
cache.hit()

print("\\n=== Polymorphism: is_healthy() on different types ===")
servers = [db, cache]
for server in servers:
    # Same call, different logic depending on object type
    healthy = "healthy" if server.is_healthy() else "needs attention"
    print(f"  {server.name}: {healthy}")

print("\\n=== str() on different types ===")
for server in servers:
    print(f"  {server}")
""".strip()

# ── File 3: oop_encapsulation.py ───────────────────────────────────

files["fundamentals/oop/oop_encapsulation.py"] = """
class ServerConfig:
    # Encapsulation: hide internal data, expose controlled interface.
    # Private attributes (prefix with _) signal: do not access directly.
    # Use properties to control read/write access.

    VALID_ENVIRONMENTS = ["development", "staging", "production"]

    def __init__(self, host, port, environment):
        self._host        = host       # _ prefix = private by convention
        self._port        = port
        self._environment = None       # set through property for validation
        self.environment  = environment  # triggers property setter

    # Property: controlled read access
    @property
    def host(self):
        return self._host

    # Property with validation
    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Port must be an integer, got {type(value).__name__}")
        if not (1 <= value <= 65535):
            raise ValueError(f"Port must be 1-65535, got {value}")
        self._port = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        if value not in self.VALID_ENVIRONMENTS:
            raise ValueError(
                f"Environment must be one of {self.VALID_ENVIRONMENTS}, got '{value}'"
            )
        self._environment = value

    def __str__(self):
        return f"ServerConfig({self._host}:{self._port} [{self._environment}])"


print("=== Encapsulation Demo ===")

config = ServerConfig("localhost", 8000, "development")
print(f"  Created: {config}")

print("\\n=== Valid property update ===")
config.port = 9000
print(f"  Updated port: {config.port}")

config.environment = "production"
print(f"  Updated env: {config.environment}")

print("\\n=== Invalid updates caught by setters ===")
try:
    config.port = "eight-thousand"
except TypeError as e:
    print(f"  TypeError: {e}")

try:
    config.port = 99999
except ValueError as e:
    print(f"  ValueError: {e}")

try:
    config.environment = "local"
except ValueError as e:
    print(f"  ValueError: {e}")

print(f"\\n  Config unchanged: {config}")
""".strip()

# ── File 4: mini_projects/server_fleet/server_fleet.py ────────────

files["mini_projects/server_fleet/__init__.py"] = ""

files["mini_projects/server_fleet/server_fleet.py"] = """
import json
from pathlib import Path
from datetime import datetime


class Server:
    MAX_CPU_THRESHOLD = 85.0

    def __init__(self, server_id, name, region, server_type, specs):
        self.server_id   = server_id
        self.name        = name
        self.region      = region
        self.server_type = server_type
        self.specs       = specs
        self.status      = "stopped"
        self.cpu_usage   = 0.0
        self.uptime_days = 0
        self._events     = []   # private event log

    def start(self):
        if self.status == "running":
            return False
        self.status = "running"
        self._log_event("started")
        return True

    def stop(self):
        if self.status == "stopped":
            return False
        self.status    = "stopped"
        self.cpu_usage = 0.0
        self._log_event("stopped")
        return True

    def update_cpu(self, usage):
        if not (0.0 <= usage <= 100.0):
            raise ValueError(f"CPU usage must be 0-100, got {usage}")
        self.cpu_usage = usage
        if usage > self.MAX_CPU_THRESHOLD:
            self._log_event(f"high_cpu_alert:{usage}%")

    def is_healthy(self):
        return self.status == "running" and self.cpu_usage < self.MAX_CPU_THRESHOLD

    def _log_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._events.append({"time": timestamp, "event": event})

    def get_events(self):
        return list(self._events)

    def to_dict(self):
        return {
            "server_id":   self.server_id,
            "name":        self.name,
            "region":      self.region,
            "type":        self.server_type,
            "status":      self.status,
            "cpu_usage":   self.cpu_usage,
            "uptime_days": self.uptime_days,
            "healthy":     self.is_healthy(),
        }

    def __str__(self):
        health = "OK" if self.is_healthy() else "ALERT"
        return (
            f"[{health}] {self.server_id} | {self.name} | "
            f"{self.region} | {self.status} | CPU: {self.cpu_usage}%"
        )

    def __repr__(self):
        return f"Server(id={self.server_id!r}, name={self.name!r})"


class ServerFleet:
    def __init__(self, fleet_name):
        self.fleet_name = fleet_name
        self._servers   = {}   # server_id -> Server object

    def add_server(self, server):
        if server.server_id in self._servers:
            raise ValueError(f"Server {server.server_id} already exists in fleet.")
        self._servers[server.server_id] = server
        print(f"  Added: {server.name} to fleet '{self.fleet_name}'")

    def remove_server(self, server_id):
        if server_id not in self._servers:
            raise KeyError(f"Server {server_id} not found in fleet.")
        removed = self._servers.pop(server_id)
        print(f"  Removed: {removed.name} from fleet.")
        return removed

    def get_server(self, server_id):
        server = self._servers.get(server_id)
        if not server:
            raise KeyError(f"Server {server_id} not found.")
        return server

    def start_all(self):
        print(f"  Starting all servers in '{self.fleet_name}'...")
        for server in self._servers.values():
            if server.start():
                print(f"    Started: {server.name}")

    def stop_all(self):
        print(f"  Stopping all servers in '{self.fleet_name}'...")
        for server in self._servers.values():
            if server.stop():
                print(f"    Stopped: {server.name}")

    def get_unhealthy(self):
        return [s for s in self._servers.values() if not s.is_healthy()]

    def get_by_region(self, region):
        return [s for s in self._servers.values() if s.region == region]

    def get_by_status(self, status):
        return [s for s in self._servers.values() if s.status == status]

    @property
    def total_servers(self):
        return len(self._servers)

    @property
    def running_count(self):
        return sum(1 for s in self._servers.values() if s.status == "running")

    def generate_report(self):
        print("=" * 58)
        print(f"  FLEET REPORT: {self.fleet_name}")
        print("=" * 58)
        print(f"  Total servers  : {self.total_servers}")
        print(f"  Running        : {self.running_count}")
        print(f"  Stopped        : {self.total_servers - self.running_count}")

        unhealthy = self.get_unhealthy()
        print(f"  Unhealthy      : {len(unhealthy)}")

        print("\\n  ALL SERVERS:")
        for server in self._servers.values():
            print(f"    {server}")

        if unhealthy:
            print("\\n  ALERTS:")
            for server in unhealthy:
                print(f"    ALERT: {server.name} | {server.status} | CPU: {server.cpu_usage}%")

        regions = {}
        for server in self._servers.values():
            regions.setdefault(server.region, 0)
            regions[server.region] += 1
        print("\\n  BY REGION:")
        for region, count in regions.items():
            print(f"    {region}: {count} server(s)")

        print("=" * 58)


if __name__ == "__main__":
    # Build the fleet
    fleet = ServerFleet("Production-US")

    fleet.add_server(Server(
        "srv-001", "api-server-01", "us-east-1", "application",
        {"cpu_cores": 4, "memory_gb": 16}
    ))
    fleet.add_server(Server(
        "srv-002", "db-server-01", "us-east-1", "database",
        {"cpu_cores": 8, "memory_gb": 32}
    ))
    fleet.add_server(Server(
        "srv-003", "cache-01", "us-west-2", "cache",
        {"cpu_cores": 2, "memory_gb": 8}
    ))
    fleet.add_server(Server(
        "srv-004", "api-server-02", "us-west-2", "application",
        {"cpu_cores": 4, "memory_gb": 16}
    ))

    print()
    fleet.start_all()

    # Simulate CPU usage
    print()
    fleet.get_server("srv-001").update_cpu(45.2)
    fleet.get_server("srv-002").update_cpu(88.9)
    fleet.get_server("srv-003").update_cpu(91.0)
    fleet.get_server("srv-004").update_cpu(32.1)

    print()
    fleet.generate_report()

    # Show events for an alerted server
    print("\\n  EVENTS for srv-002:")
    for event in fleet.get_server("srv-002").get_events():
        print(f"    [{event['time']}] {event['event']}")
""".strip()

# ── Write all files ────────────────────────────────────────────────

for filepath, content in files.items():
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")

print("\\nAll Day 7 files created successfully.")