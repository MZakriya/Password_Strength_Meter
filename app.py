import streamlit as st
import re
import secrets
import string

# List of common weak passwords
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "monkey", "sunshine"]

# Function to check for common passwords
def is_common_password(password):
    return password.lower() in COMMON_PASSWORDS

# Function to check for repetitive patterns
def has_repetitive_pattern(password):
    return re.search(r'(.)\1{2,}', password) is not None

# Function to check for keyboard patterns
def has_keyboard_pattern(password):
    keyboard_patterns = [
        "qwertyuiop", "asdfghjkl", "zxcvbnm", 
        "1234567890", "!@#$%^&*()"
    ]
    password_lower = password.lower()
    for pattern in keyboard_patterns:
        if password_lower in pattern or password_lower in pattern[::-1]:
            return True
    return False

# Function to calculate password entropy
def calculate_entropy(password):
    if not password:
        return 0
    # Character pool size
    pool_size = 0
    if re.search(r'[a-z]', password):
        pool_size += 26
    if re.search(r'[A-Z]', password):
        pool_size += 26
    if re.search(r'[0-9]', password):
        pool_size += 10
    if re.search(r'[!@#$%^&*]', password):
        pool_size += 8
    # Entropy formula: log2(pool_size^length)
    entropy = len(password) * (pool_size ** 0.5)
    return entropy

# Function to evaluate password strength
def evaluate_password_strength(password):
    score = 0

    # Criteria checks
    length_check = len(password) >= 8
    uppercase_check = bool(re.search(r'[A-Z]', password))
    lowercase_check = bool(re.search(r'[a-z]', password))
    digit_check = bool(re.search(r'[0-9]', password))
    special_char_check = bool(re.search(r'[!@#$%^&*]', password))

    # Assign scores based on criteria
    if length_check:
        score += 1
    if uppercase_check:
        score += 1
    if lowercase_check:
        score += 1
    if digit_check:
        score += 1
    if special_char_check:
        score += 1

    # Penalize for common passwords, repetitive patterns, or keyboard patterns
    if is_common_password(password):
        score -= 2
    if has_repetitive_pattern(password):
        score -= 1
    if has_keyboard_pattern(password):
        score -= 1

    # Ensure score doesn't go below 0
    score = max(score, 0)

    # Calculate entropy
    entropy = calculate_entropy(password)

    return score, entropy

# Function to generate a strong password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

# Function to provide feedback based on score
def get_strength_feedback(score, entropy, password):
    if score == 5 and entropy > 50:
        return "Strong: Your password meets all security criteria. Great job!"
    elif score >= 3:
        feedback = "Moderate: Your password is decent but could be improved.\n"
    else:
        feedback = "Weak: Your password is too simple and insecure.\n"

    # Add specific feedback for missing criteria
    if len(password) < 8:
        feedback += "- Make it at least 8 characters long.\n"
    if not re.search(r'[A-Z]', password):
        feedback += "- Add at least one uppercase letter.\n"
    if not re.search(r'[a-z]', password):
        feedback += "- Add at least one lowercase letter.\n"
    if not re.search(r'[0-9]', password):
        feedback += "- Include at least one digit.\n"
    if not re.search(r'[!@#$%^&*]', password):
        feedback += "- Add at least one special character (!@#$%^&*).\n"
    if is_common_password(password):
        feedback += "- Avoid using common passwords.\n"
    if has_repetitive_pattern(password):
        feedback += "- Avoid repetitive patterns.\n"
    if has_keyboard_pattern(password):
        feedback += "- Avoid keyboard patterns.\n"

    return feedback

# Streamlit app
def main():
    # Sidebar - About section
    st.sidebar.title("About")
    st.sidebar.write("""
    ### Password Strength Meter 🔒
    This app evaluates the strength of your password based on:
    - **Length**: At least 8 characters.
    - **Character Types**: Uppercase, lowercase, digits, and special characters.
    - **Patterns**: Avoids common passwords, repetitive patterns, and keyboard patterns.
    - **Entropy**: Measures password unpredictability.

    #### How to Use:
    1. Enter your password in the input box.
    2. The app will evaluate its strength and provide feedback.
    3. Use the **Generate Strong Password** button to create a secure password.

    #### Why Password Strength Matters:
    A strong password protects your accounts from unauthorized access and cyberattacks. Always use unique, complex passwords for each account
    
    #### Made with ❤️ by Muhammad Zakriya.  
    Feel free to reach out for feedback or suggestions!
    """)

    # Main content
    st.title("Password Strength Meter 🔒")
    st.write("Enter your password below to check its strength.")

    # Password input
    password = st.text_input("Enter your password:", type="password")

    # Generate strong password button
    if st.button("Generate Strong Password"):
        strong_password = generate_strong_password()
        st.text_area("Generated Password:", strong_password)

    if password:
        # Evaluate password strength
        score, entropy = evaluate_password_strength(password)
        feedback = get_strength_feedback(score, entropy, password)

        # Display score and feedback
        st.subheader("Password Strength:")
        if score == 5 and entropy > 50:
            st.success(feedback)
        elif score >= 3:
            st.warning(feedback)
        else:
            st.error(feedback)

        # Visual representation of strength
        st.progress(score / 5)

# Run the app
if __name__ == "__main__":
    main()