"""
Defines which message categories each user role is allowed to access.
Used to decide whether a classified message should be handled by the agent
or rejected with an access-denied response.
"""

Permission = {
    "guest" : ["SERVICE"],
    "admin" : ["SERVICE", "MAINTENANCE", "SOS"]
}

def is_allowed (role, category):
    return category in Permission.get(role, [])
