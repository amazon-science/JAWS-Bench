from user_activity import record_login, record_logout, record_action

def main():
    # Example usage
    user_id = "user123"
    record_login(user_id)
    record_action(user_id, "viewed profile")
    record_action(user_id, "edited settings")
    record_logout(user_id)

if __name__ == "__main__":
    main()