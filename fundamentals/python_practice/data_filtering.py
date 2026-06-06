response_times = [120, 340, 89, 210, 456, 78, 390, 145]

def analyze_response_times(times, threshold):
    slow_responses = []
    for time in times:
        if time > threshold:
            slow_responses.append(time)
    print("Slow responses:", slow_responses)
    print(f"Total slow responses: {len(slow_responses)}")
    print(f"Slowest response: {max(times)}ms")
    print(f"Fastest response: {min(times)}ms")
    average = sum(times) / len(times)
    print(f"Average response time: {average}ms")
    average_slow = sum(slow_responses) / len(slow_responses) if slow_responses else 0
    print(f"Average slow response time: {average_slow}ms")

analyze_response_times(response_times, 200)
analyze_response_times(response_times, 300)