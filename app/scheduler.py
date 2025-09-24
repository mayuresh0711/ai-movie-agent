from app.controllers import user_controller, recommend_controller

def send_recommendations_to_all_users():
    """
    This is the main job the scheduler will run.
    """
    print("SCHEDULER: Starting job to send recommendations to all users...")
    
    users = user_controller.get_all_users()
    
    if not users:
        print("SCHEDULER: No users found in the database. Job finished.")
        return

    print(f"SCHEDULER: Found {len(users)} users. Processing now...")

    for user in users:
        user_id = user.get("id")
        user_name = user.get("name")
        print(f"SCHEDULER: Generating and sending email to {user_name} (ID: {user_id})...")
        
        # We reuse the function we already built!
        status = recommend_controller.send_recommendation_email(user_id)
        
        if "error" in status:
            print(f"SCHEDULER: FAILED to send email to {user_name}. Reason: {status['error']}")
        else:
            print(f"SCHEDULER: Successfully sent email to {user_name}.")

    print("SCHEDULER: All users processed. Job finished.")