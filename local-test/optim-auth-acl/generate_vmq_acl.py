import base64

def generate_vmq_acl(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_user = None
        for line in infile:
            # Strip whitespace
            line = line.strip()

            # Skip entire comment lines or empty lines
            if not line or line.startswith('#'):
                continue

            # Split the line into exactly 4 comma-separated parts
            parts = [part.strip() for part in line.split(',')]
            
            # Ensure there are exactly 4 parts
            if len(parts) != 4:
                print(f"Skipping malformed line: {line}")
                continue

            user, permission, topic, access = parts
            
            # Validate that access is either '0' or '1'
            if access not in {'0', '1'}:
                print(f"Skipping line with invalid access value: {line}")
                continue

            # Check if we're writing rules for a new user
            if user != current_user:
                # Write the user line only once per user
                outfile.write(f"user {user}\n")
                current_user = user

            # Write the ACL rule based on permission type and access (allow or deny)
            if permission == 'subscribe':
                outfile.write(f"topic {topic}\nsubscribe {access}\n")
            elif permission == 'publish':
                outfile.write(f"topic {topic}\npublish {access}\n")
            else:
                print(f"Skipping line with invalid permission: {line}")

    print(f"{output_file} generated successfully.")

def encode_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_content = base64.b64encode(file.read()).decode('utf-8')

    print("Base64 encoded content for Kubernetes secret:")
    print(encoded_content)

# Input and output file names
input_file = "./input/useracl.txt"      # Input plain text file with ACL rules
output_file = "./output/vmq.acl"        # Output file for VerneMQ ACL

# Generate the vmq.acl file
generate_vmq_acl(input_file, output_file)

# Encode the output file in base64 for Kubernetes secret
encode_base64(output_file)
