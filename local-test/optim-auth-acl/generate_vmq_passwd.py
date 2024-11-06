import hashlib
import base64

def generate_vmq_passwd(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            user, password = line.strip().split(',')
            
            # Hash the password with SHA-256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Write to vmq.passwd format
            outfile.write(f"{user}:{hashed_password}\n")
    
    print(f"{output_file} generated successfully.")

def encode_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_content = base64.b64encode(file.read()).decode('utf-8')
    
    print("Base64 encoded content for Kubernetes secret:")
    print(encoded_content)

# Input and output file names
input_file = "./input/userpasswd.txt"    # Input plain text file with usernames and passwords
output_file = "./output/vmq.passwd"       # Output file for VerneMQ

# Generate the vmq.passwd file
generate_vmq_passwd(input_file, output_file)

# Encode the output file in base64 for Kubernetes secret
encode_base64(output_file)
