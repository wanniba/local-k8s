Here’s a `README.md` file for your project, explaining the purpose of the scripts, how to use them, and the required input format.

```markdown
# VerneMQ Authentication and ACL Generation

This project provides Python scripts to generate VerneMQ password and ACL files (`vmq.passwd` and `vmq.acl`), and to encode them in base64 for storage as Kubernetes secrets. The scripts process input files with user credentials and ACL rules, respectively, to create VerneMQ-compatible authentication and access control files.

## Files

- `generate_vmq_passwd.py`: Generates a `vmq.passwd` file from a plain text file with username and password pairs, hashed with SHA-256.
- `generate_vmq_acl.py`: Generates a `vmq.acl` file from a plain text file with ACL rules, specifying user permissions for VerneMQ topics.

## Requirements

- Python 3.x
- The following modules, which are part of the Python standard library:
  - `hashlib`
  - `base64`

## Directory Structure

Your project directory should be organized as follows:

```
.
├── input/
│   ├── userpasswd.txt  # Input file with username and passwords for authentication
│   └── useracl.txt     # Input file with user ACL rules
├── output/
│   ├── vmq.passwd      # Generated VerneMQ password file
│   └── vmq.acl         # Generated VerneMQ ACL file
├── generate_vmq_passwd.py
├── generate_vmq_acl.py
└── README.md
```

## Usage

### 1. Generate the `vmq.passwd` File

The `generate_vmq_passwd.py` script reads the `input/userpasswd.txt` file, hashes the passwords with SHA-256, and writes them in `user:hashed_password` format to `output/vmq.passwd`. It then encodes the file in base64 for use as a Kubernetes secret.

#### `userpasswd.txt` Format

Each line in `userpasswd.txt` should contain a username and password, separated by a comma, in the following format:

```
username1,password1
username2,password2
...
```

#### Run the Script

```bash
python generate_vmq_passwd.py
```

The script outputs the base64-encoded content of `vmq.passwd` for use in Kubernetes secrets.

### 2. Generate the `vmq.acl` File

The `generate_vmq_acl.py` script reads the `input/useracl.txt` file and writes ACL rules to `output/vmq.acl`, then encodes the file in base64 for Kubernetes secrets.

#### `useracl.txt` Format

Each line in `useracl.txt` should contain the following four values, separated by commas:

```
username,permission,topic,access
```

- `username`: The name of the user (e.g., `deviceUser`, `adminUser`).
- `permission`: Either `subscribe` or `publish`.
- `topic`: The MQTT topic (e.g., `devices/+/status`, `logs/#`).
- `access`: `1` for allowed access, `0` for denied access.

#### Example `useracl.txt`

```plaintext
deviceUser,subscribe,devices/+/status,1
deviceUser,publish,devices/+/data,1
deviceUser,publish,CTRL,0
adminUser,subscribe,#,1
adminUser,publish,#,1
adminUser,publish,system/commands,1
adminUser,subscribe,logs/#,1
opUser,subscribe,system/monitoring,1
opUser,subscribe,logs/errors,1
opUser,publish,system/alerts,1
```

#### Run the Script

```bash
python generate_vmq_acl.py
```

The script outputs the base64-encoded content of `vmq.acl` for use in Kubernetes secrets.

## Example Kubernetes Secret

To use the generated files as Kubernetes secrets, copy the base64 output from each script and use it in your Kubernetes YAML file:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: vernemq-auth-secrets
type: Opaque
data:
  vmq.passwd: <base64-encoded-content-from-generate_vmq_passwd.py>
  vmq.acl: <base64-encoded-content-from-generate_vmq_acl.py>
```

Replace `<base64-encoded-content-from-generate_vmq_passwd.py>` and `<base64-encoded-content-from-generate_vmq_acl.py>` with the actual base64 output from each script.

## Notes

- Ensure that the `input/` and `output/` directories exist before running the scripts.
- Verify that `userpasswd.txt` and `useracl.txt` files are correctly formatted to avoid errors during processing.
- These scripts are intended for environments where VerneMQ is used with Kubernetes, but the generated files can also be used directly in any VerneMQ deployment.

