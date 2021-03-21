def find_max_sum(arr):
    
    curr_max = 0
    curr = 0
 
    for ele in arr:
        curr += ele
 
        if curr > curr_max:
            curr_max = curr
 
    return curr_max
 
T = int(input())
for t in range(T):
 
    health_values = []
 
    N, M = [int(x) for x in input().split()]
 
    max_health = 0
 
    for n in range(N):
        health_values.append([int(x) for x in input().split()])
 
    dp = [{'l': 0, 'r': 0} for _ in range(N)]
 
    dp[0]['l'] = find_max_sum(health_values[0])
    dp[0]['r'] = sum(health_values[0])
 
    for n in range(1, N):
        dp[n]['l'] = max(dp[n - 1]['r'] + sum(health_values[n]), dp[n - 1]['l'] + find_max_sum(health_values[n]))
 
        dp[n]['r'] = max(dp[n - 1]['l'] + sum(health_values[n]), dp[n - 1]['r'] + find_max_sum(health_values[n][::-1]))
 
    print(max(dp[N - 1]['l'], dp[N - 1]['r']))
