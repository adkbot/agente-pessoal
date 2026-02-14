
import os

def sanitize_file(filepath):
    print(f"Sanitizing {filepath}...")
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Remove null bytes
        clean_content = content.replace(b'\x00', b'')
        
        # Remove potential BOMs
        if clean_content.startswith(b'\xff\xfe'):
            clean_content = clean_content[2:]
        if clean_content.startswith(b'\xfe\xff'):
            clean_content = clean_content[2:]
        if clean_content.startswith(b'\xef\xbb\xbf'):
            clean_content = clean_content[3:]
            
        # Decode and re-encode to ensure valid UTF-8
        text = clean_content.decode('utf-8', errors='ignore')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
            
        print("Sanitization complete.")
        
        # Verify
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f"First 100 chars: {f.read()[:100]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sanitize_file("skills.py")
