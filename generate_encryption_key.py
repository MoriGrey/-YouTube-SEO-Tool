"""
Generate encryption key for Streamlit Cloud Secrets
"""

from src.utils.encryption import EncryptionManager

# Generate key
key = EncryptionManager.generate_key()

print("=" * 60)
print("ENCRYPTION KEY FOR STREAMLIT CLOUD SECRETS")
print("=" * 60)
print()
print("Copy the following line and paste it into Streamlit Cloud Secrets:")
print()
print(f'ENCRYPTION_KEY = "{key}"')
print()
print("=" * 60)
print("IMPORTANT: Keep this key secure and don't share it publicly!")
print("=" * 60)

