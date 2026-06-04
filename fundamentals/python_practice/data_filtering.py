# A list of numbers representing response times in milliseconds
response_times = [120, 340, 89, 210, 456, 78, 390, 145]

# Print all response times
for time in response_times:
    print(time)

    # Filter response times above 200ms
slow_responses = []

for time in response_times:
    if time > 200:
        slow_responses.append(time)

print("Slow responses:", slow_responses)

# Count how many slow responses
print(f"Total slow responses: {len(slow_responses)}")

# Find the slowest response
print(f"Slowest response: {max(response_times)}ms")

# Find the fastest response
print(f"Fastest response: {min(response_times)}ms")

# Calculate average response time
average = sum(response_times) / len(response_times)
print(f"Average response time: {average}ms")

average_slow = sum(slow_responses) / len(slow_responses) if slow_responses else 0
print(f"Average slow response time: {average_slow}ms")