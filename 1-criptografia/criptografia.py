import hashlib

def main():
    msg = input('alooo')
    hsh = hashlib.sha1()

    hsh.update(msg.encode('utf-8'))
    
    print(hsh.hexdigest())

if __name__ == "__main__":
    main()