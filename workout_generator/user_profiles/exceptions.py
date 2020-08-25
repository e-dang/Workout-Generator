class InvalidFollowRequest(Exception):
    """
    Raised when a UserProfile tries to handle a FollowRequest where they are not the target profile.
    """
