import hashlib

# Create your tests here.

def hash_code(s, salt='nyanpasu'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
print(hash_code('jinl1874'))