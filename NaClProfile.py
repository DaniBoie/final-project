# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin


# TODO: Install the pynacl library so that the following modules are available
# to your program.
import copy
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

# TODO: Import the Profile and Post classes
from Profile import Profile
from Profile import Post
# TODO: Import the NaClDSEncoder module
from NaClDSEncoder import NaClDSEncoder
from base64 import binascii
    

# TODO: Subclass the Profile class
class NaClProfile(Profile):
    def __init__(self):
        super().__init__()
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        self.public_key = None
        self.private_key = None
        self.keypair = None


    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """
        # create an NaClDSEncoder object
        nacl_enc = NaClDSEncoder()
        # generate new keys
        nacl_enc.generate()

        self.keypair = nacl_enc.keypair
        self.public_key = nacl_enc.public_key
        self.private_key = nacl_enc.private_key
        return self.keypair


    def import_keypair(self, keypair: str) -> None:
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        try:
            assert type(keypair) == str
        except AssertionError:
            print("Keypair not of type Str.")
            return

        try:
            assert len(keypair) == 88
        except AssertionError:
            print("Keypair not of length 88")
            return

        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair[44:]
        pass


    def add_post(self, post: Post) -> None:
        """
        TODO: Override the add_post method to encrypt post entries.

        Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
        code that is already written in the parent class.

        NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:
        
        super().add_post(...)
        """
        post.entry = self._encrypt_message(post.entry, self.private_key, self.public_key)
        self._posts.append(post)


    def get_posts(self) -> list:
        """
        TODO: Override the get_posts method to decrypt post entries.

        Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
        decrypted before returning them to the calling code.

        :return: Post
        
        NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
        super().get_posts()
        """
        # Creates a copied list to not modify the contents of the original _posts list.
        copied_list = copy.deepcopy(self._posts)
        for post in copied_list:
            try:
                post.entry = self._decrypt_message(post.entry, self.private_key, self.public_key)
            except AttributeError:
                print("Error decoding posts.")
                return False
        return copied_list
    
    def load_profile(self, path: str) -> None:
        """
        TODO: Override the load_profile method to add support for storing a keypair.

        Since the DS Server is now making use of encryption keys rather than username/password attributes, you will need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
        load_profile module and add any new attributes you wish to support.

        NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO. Just add support for your new attributes.
        """
        # Added new attributes to parent class and took super() to call it.
        super().load_profile(path)

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        
        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts and this method can call.
        
        :return: bytes 
        """
        message = None
        try:
            assert type(public_key) == str
        except AssertionError:
            print("Public key not of type str.")
            return
        
        try:
            assert type(entry) == str
        except AssertionError:
            print("Message entry not of type Str.")
            return
        # Uses defined __encrypt_message() function to use the user's private key and another public key to encrypt a message.
        try:
            message = self._encrypt_message(entry, self.private_key, public_key)
        except binascii.Error:
            print("String not a key.")
            return
        except nacl.exceptions.ValueError:
            print("Public key is less than 32 Bytes.")
            return

        if message == None:
            return
        else:
            # _encrypt_message() returns ASCII formatting so this turns it back into bytes.
            return message.encode(encoding='UTF-8')
        

    def _encrypt_message(self, entry: str, private_key: str, public_key: str) -> str:
        '''
        Takes a message, private, and public key and encrypts the message using the NaClDSEncoder() and the nacl library.
        '''
        try:
            assert type(public_key) == str
        except AssertionError:
            print("public key not of type Str.")
            return

        bpost = entry.encode(encoding='UTF-8')  # converts str to bytes
        encoder = NaClDSEncoder()
        # Encodes keys using NaCl Encoder method provided.
        encoded_priv = encoder.encode_private_key(private_key)
        encoded_pub = encoder.encode_public_key(public_key)

        # user's priv key and either user's public key or someone else's public key
        box = Box(encoded_priv, encoded_pub)
        bencrypted_message = box.encrypt(bpost, encoder=nacl.encoding.Base64Encoder)  # encrypted message in bytes

        encrypted_message = bencrypted_message.decode(encoding='UTF-8')  # changes to alphanumeric

        return encrypted_message

    def _decrypt_message(self, encrypted_message:str, private_key: str, public_key: str) -> str:
        '''
        Takes a message, private, and public key and decrypts the message using the NaClDSEncoder() and the nacl library.
        '''
        bencrypted_message = encrypted_message.encode(encoding='UTF-8') # converts str to bytes
        
        # Uses NaCl Encoder methods to encode public and private keys.
        encoder = NaClDSEncoder()
        encoded_priv = encoder.encode_private_key(private_key)
        encoded_pub = encoder.encode_public_key(public_key)

        box = Box(encoded_priv, encoded_pub)  # Same keys as encrpytion

        bpost = box.decrypt(bencrypted_message, encoder=nacl.encoding.Base64Encoder)

        post = bpost.decode(encoding = 'UTF-8')

        return post

if __name__ == "__main__":
    man = NaClProfile()
    man.generate_keypair()
    message = "hello"
    encrypted = man.encrypt_entry("hello", man.public_key)
    print(encrypted)
    encrypted = encrypted.decode(encoding='UTF-8')
    decrypted = man._decrypt_message(encrypted, man.private_key, man.public_key)
    print(decrypted)
    
