from server.clients import clients

# Function to get the current number of connected clients
def get_connected_clients():
    return len(clients)

# Function to generate basic stats (you can extend this later)
def get_dashboard_stats():
    connected_count = get_connected_clients()
    stats = {
        "connected_clients": connected_count,
        # You can add more stats like message count, etc., here
    }
    return stats
