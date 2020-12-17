import unittest

from twitch.oauth import *


class TestOauth(unittest.TestCase):

    # If test_check_token passes, then we can assume the other tests will work
    def test_check_token(self):
        self.assertTrue(check_token('REDACTED'))
    
    def test_check_fake_token(self):
        self.assertFalse(check_token('jhdxeqkv27zdbxepye1i7ugmfbl1rb'))
    
    def test_get_token(self):
        token = get_token('zftyh5nye97uv9acvym1gaoulhxcg7')
        self.assertTrue(check_token(token))
    
    def test_revoke_token(self):
        token = get_token('zftyh5nye97uv9acvym1gaoulhxcg7')
        self.assertTrue(check_token(token))
        revoke_token('zftyh5nye97uv9acvym1gaoulhxcg7', token)
        self.assertFalse(check_token(token))
    
    def test_revoke_fake_token(self):
        token = 'x19o1k8d681p4xrc3vdtmphm7xf189'
        self.assertFalse(check_token(token))
        revoke_token('zftyh5nye97uv9acvym1gaoulhxcg7', token)
        self.assertFalse(check_token(token))


if __name__ == "__main__":
    unittest.main()