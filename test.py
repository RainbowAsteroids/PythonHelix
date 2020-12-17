import unittest

import twitch.oauth


class TestOauth(unittest.TestCase):

    # If test_check_token passes, then we can assume the other tests will work
    def test_check_token(self):
        self.assertTrue(twitch.oauth.check_token('REDACTED'))

    def test_check_fake_token(self):
        self.assertFalse(
            twitch.oauth.check_token('jhdxeqkv27zdbxepye1i7ugmfbl1rb')
        )

    def test_get_token(self):
        token = twitch.oauth.get_token('zftyh5nye97uv9acvym1gaoulhxcg7')
        self.assertTrue(twitch.oauth.check_token(token))

    def test_revoke_token(self):
        token = twitch.oauth.get_token('zftyh5nye97uv9acvym1gaoulhxcg7')
        self.assertTrue(twitch.oauth.check_token(token))
        twitch.oauth.revoke_token('zftyh5nye97uv9acvym1gaoulhxcg7', token)
        self.assertFalse(twitch.oauth.check_token(token))

    def test_revoke_fake_token(self):
        token = 'x19o1k8d681p4xrc3vdtmphm7xf189'
        self.assertFalse(twitch.oauth.check_token(token))
        twitch.oauth.revoke_token('zftyh5nye97uv9acvym1gaoulhxcg7', token)
        self.assertFalse(twitch.oauth.check_token(token))


if __name__ == "__main__":
    unittest.main()
