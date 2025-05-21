import datetime
import uuid
import matplotlib.pyplot as plt
from tabulate import tabulate

# Structure: {user_id: {...user data...}}
social_data = {}

def generate_user_id():
    return str(uuid.uuid4())[:8]  # Short unique ID

def create_post(post_number):
    """Create one post entry with labeled input."""
    print(f"\n🔸 Enter details for Post #{post_number}:")
    post = {
        "post_id": input("  ➤ Post ID or Title: "),
        "comments": int(input("  ➤ Number of comments: ")),
        "likes": int(input("  ➤ Number of likes: ")),
        "shares": int(input("  ➤ Number of shares: ")),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return post

def insert_users():
    """Insert multiple user records."""
    n = int(input("How many user records do you want to enter? "))

    for i in range(n):
        print(f"\n📝 Entering data for User #{i+1}")
        name = input("➤ Name: ")

        while True:
            contact = input("➤ Contact Number: ")
            if contact.isdigit() and len(contact) == 10:
                break
            print("❌ Invalid input. Please enter a 10-digit number.")

        linkedin_id = input("➤ LinkedIn ID: ")
        connections = int(input("➤ Number of LinkedIn Connections: "))
        active_time = input("➤ Active Time on Platform (e.g., 2h/day): ")

        num_posts = int(input("➤ How many posts to enter? "))
        posts = []
        for j in range(num_posts):
            posts.append(create_post(j + 1))

        user_id = generate_user_id()
        social_data[user_id] = {
            "name": name,
            "contact": contact,
            "linkedin_id": linkedin_id,
            "connections": connections,
            "active_time": active_time,
            "posts": posts,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(f"\n✅ User '{name}' inserted successfully!")
        print(f"🆔 Unique User ID: {user_id}\n")

def display_data():
    """Display all user data."""
    if not social_data:
        print("⚠️ No data available.\n")
        return

    headers = ["User ID", "Name", "Contact", "LinkedIn ID", "Connections", "Post ID", "Comments", "Likes", "Shares", "Post Time", "Active Time", "User Created"]
    table = []

    for user_id, data in social_data.items():
        for post in data["posts"]:
            table.append([
                user_id,
                data["name"],
                data["contact"],
                data["linkedin_id"],
                data["connections"],
                post["post_id"],
                post["comments"],
                post["likes"],
                post["shares"],
                post["timestamp"],
                data["active_time"],
                data["created_at"]
            ])

    print(tabulate(table, headers=headers, tablefmt="grid"))

def modify_post():
    """Modify a post by User ID and Post ID."""
    user_id = input("Enter User ID: ")
    if user_id not in social_data:
        print("❌ User not found.\n")
        return

    post_id = input("Enter Post ID to modify: ")
    for post in social_data[user_id]["posts"]:
        if post["post_id"] == post_id:
            print("Leave blank to keep value.")
            for field in ["comments", "likes", "shares"]:
                new_val = input(f"{field.capitalize()} (current: {post[field]}): ")
                if new_val.strip():
                    post[field] = int(new_val)
            post["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("✅ Post updated.\n")
            return

    print("❌ Post ID not found.\n")

def fetch_user_summary():
    """Display summary of engagement for a user."""
    user_id = input("Enter User ID: ")
    if user_id not in social_data:
        print("❌ User not found.\n")
        return

    user = social_data[user_id]
    total_comments = total_likes = total_shares = 0

    for post in user["posts"]:
        total_comments += post["comments"]
        total_likes += post["likes"]
        total_shares += post["shares"]

    summary = [
        ["Name", user["name"]],
        ["Contact", user["contact"]],
        ["LinkedIn ID", user["linkedin_id"]],
        ["Connections", user["connections"]],
        ["Active Time", user["active_time"]],
        ["Total Posts", len(user["posts"])],
        ["Total Comments", total_comments],
        ["Total Likes", total_likes],
        ["Total Shares", total_shares],
    ]

    print(f"\n📊 Engagement Summary for User ID: {user_id}")
    print(tabulate(summary, headers=["Field", "Value"], tablefmt="fancy_grid"))

    # Plotting the engagement per post
    post_ids = [post["post_id"] for post in user["posts"]]
    likes = [post["likes"] for post in user["posts"]]
    comments = [post["comments"] for post in user["posts"]]
    shares = [post["shares"] for post in user["posts"]]

    x = range(len(post_ids))
    width = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar([i - width for i in x], likes, width=width, label='Likes', color='skyblue')
    plt.bar(x, comments, width=width, label='Comments', color='lightgreen')
    plt.bar([i + width for i in x], shares, width=width, label='Shares', color='salmon')

    plt.xlabel("Post ID")
    plt.ylabel("Engagement Count")
    plt.title(f"Engagement Metrics for User '{user['name']}'")
    plt.xticks(ticks=x, labels=post_ids, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\n=== 📈 Social Media Analytical Dashboard ===")
        print("1. Insert New Users and Posts")
        print("2. Display All User Data")
        print("3. Modify a User Post")
        print("4. Fetch User Engagement Summary")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            insert_users()
        elif choice == '2':
            display_data()
        elif choice == '3':
            modify_post()
        elif choice == '4':
            fetch_user_summary()
        elif choice == '5':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
